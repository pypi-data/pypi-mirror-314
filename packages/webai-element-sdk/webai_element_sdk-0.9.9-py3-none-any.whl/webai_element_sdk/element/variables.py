import asyncio
import json
import os
from collections.abc import AsyncIterator
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict, dataclass, field
from typing import Any, Dict, Generic, List, Optional, Tuple, Type, TypeVar, get_origin, get_args
import uuid

import msgspec
import numpy as np

from webai_element_sdk.comms.messages import Preview, TextFrame, ImageFrame, MLXFrame, Frame
from webai_element_sdk.runner import ElementClient as ElementClient
from webai_element_sdk.runner import ElementSocketServer as ElementServer

executor = ThreadPoolExecutor()
decoder = msgspec.json.Decoder()
encoder = msgspec.json.Encoder()

packdecoder = msgspec.msgpack.Decoder()
packencoder = msgspec.msgpack.Encoder()

T = TypeVar("T")

HOST_OUTPUT_KEYS = os.getenv("HOST_OUTPUT_KEYS")
ENABLE_LOSSLESS = os.getenv("ENABLE_LOSSLESS")
# TODO: determine if this wrapper is even necessary

@dataclass
class Variable(Generic[T]):
    """Input/Output data type base class

    Attributes:
        name (Optional[str]): TODO
        value (Optional[T]): TODO
    """

    name: Optional[str] = field(init=False, default=None)
    value: Optional[T] = field(init=False, default=None)

    @property
    def type(self) -> Type[T]:
        return self.__orig_class__.__args__[0]  # type: ignore

    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result["type"] = self.type
        return result


@dataclass
class Input(Variable[T]):
    """Element input definition data type"""

    def __call__(self, value: Optional[T] = None):
        self.value = value
        return self


@dataclass
class Output(Variable[T]):
    """Element output definition data type"""

    def __call__(self, value: Optional[T] = None):
        return self, value

    def setup(self, output_slots: Dict[str, List[Dict[str, str]]], host_by_key: Dict[str, str]):
        if self.type is Preview:
            return

        if self.name not in output_slots or output_slots[self.name] is None:
            raise Exception("No output slot with required name")

        self._client = ElementClient(ENABLE_LOSSLESS == "1")
        self._client.start(output_slots[self.name], host_by_key)

    def close(self):
        if self.type is Preview:
            return
        self._client.send_close()

    async def send(self, value: Frame):
        self.send_frame(value)

    def send_frame(self, frame: Frame):
        """send add_frame message"""

        jsonreq = {
            "frame_id": str(frame.frame_id),
            "headers": frame.headers,
            "other_data": json.dumps(frame.other_data),
        }

        if frame.content_type == "mlx-frame":
            self._client.send(3, "default", jsonreq, "add_frame", frame.content_type, frame.content_bytes, b"")
            return

        if frame.content_type == "mlx":
            self._client.send(3, "default", jsonreq, "add_frame", frame.content_type, frame.array, b"")
            return

        if frame.content_type == "text":
            self._client.send(3, "default", jsonreq, "add_frame", frame.content_type, str.encode(frame.text, 'utf-8'), b"")
            return

        if frame.ndframe is None: # legacy text frame
            self._client.send(1, "default", jsonreq, "add_frame", frame.content_type, b"", b"")
            return

        # legacy and current image frame
        rois = [roi.to_dict() for roi in frame.rois]
        roi_pack = packencoder.encode(rois)

        content = frame.ndframe.tobytes()

        jsonreq = jsonreq | {
            "height": frame.ndframe.shape[0],
            "width": frame.ndframe.shape[1],
            "channels": frame.ndframe.shape[2],
            "dtype": str(frame.ndframe.dtype),
            "color_space": frame.color_space.name,
            "rois": rois,
        }
        self._client.send(3, "default", jsonreq, "add_frame", frame.content_type, content, roi_pack)


V = TypeVar("V", Input[Any], Output[Any])
"""Input/Output type generic"""


class Variables(Generic[V]):
    """Abstract class for Input/Output pluralization"""

    def __init__(self):
        for name, variable in self.to_dict().items():
            variable.name = name

    def __getitem__(self, name: str) -> V:
        return getattr(self, name)

    def __setitem__(self, name: str, value: V):
        setattr(self, name, value)

    @classmethod
    def to_dict(cls) -> Dict[str, V]:
        result: Dict[str, V] = dict()
        for field_name, field in vars(cls).items():
            if isinstance(field, Variable):
                result[field_name] = field  # type: ignore
        return result


class ElementInputs(Variables[Input[Any]]):
    """Abstract class to be extended with Element Input fields

    Example:
        ```py
        class MyInputs(ElementInputs):
            input1 = Input[Frame]()
        ```
    """

    _receiver: ElementServer | None

    def __init__(self):
        super().__init__()
        # TODO pass slot names to server to set up listeners for each

    def setup(self, callback: Any):
        server_port = os.getenv("ELEMENT_SERVER_PORT")
        if not server_port:
            raise Exception("No element server port set")
        self._receiver = ElementServer()
        self._receiver.start(f"0.0.0.0:{server_port}", ENABLE_LOSSLESS == "1")

    def is_v0_slot(self, slot_name):
        type = self[slot_name].type
        return True if type is Frame else (get_args(type)[0] is Frame)


    async def receive(self, callback: Any):
        if self._receiver is None:
            return
        receiver_gen = self.wait_for_frame()
        async for received in receiver_gen:
            # Special case for power user
            if get_origin(self[received[0]].type) == AsyncIterator:

                async def payload_receiver() -> AsyncIterator[Any]:
                    first_frame = None
                    async for r in receiver_gen:
                        if not first_frame:
                            first_frame = received[1]
                            yield first_frame
                        yield r[1]

                payload_receiver_gen = payload_receiver()
                # set the input here
                input = self[received[0]](payload_receiver_gen)
                await callback()  # <== Long running since rcvr provided
                break

            # Set input field based on name
            input = self[received[0]](received[1])

            if input.value is not None:
                await callback()

    async def wait_for_frame(self) -> AsyncIterator[Tuple[str, Frame]]:
        """wait for frame"""
        if self._receiver is None:
            return
        while True:
            loop = asyncio.get_running_loop()
            frame = await loop.run_in_executor(executor, self._receiver.wait_for_frame)

            content = frame[0]
            content2 = frame[1]
            json_data = frame[2]
            slot = frame[3]
            content_type = frame[4] if len(frame) == 5 else None

            # account for fw versions that either don't send content_type or pass it upwards as empty string
            if content_type is None or len(content_type) == 0:
                content_type = "text"

            json = decoder.decode(json_data)

            frame_id = None
            if "frame_id" in json and json["frame_id"]:
                try:
                    frame_id = uuid.UUID(json["frame_id"])
                except ValueError:
                    pass  # Invalid UUID, frame_id remains None
            headers = json["headers"] if "headers" in json else dict()
            other_data = decoder.decode(json["other_data"] if "other_data" in json and len(json["other_data"]) > 0 else "{}")

            # v0 element receives v0 or v1 frame
            if self.is_v0_slot(slot):
                if content_type == "text" or Frame.is_text(content_type, other_data):
                    yield slot, Frame.as_text(frame_id, headers, other_data, content)
                    continue

                if content_type == "image" or Frame.is_image(content_type, json):
                    yield slot, Frame.as_image(frame_id, headers, other_data, json, content, content2)
                    continue

                if content_type == "mlx" or Frame.is_mlx(content_type, content, content2):
                    yield slot, Frame.as_mlx(frame_id, headers, other_data, content)
                    continue

            # v1 element receives v0 frame
            if content_type == "cv2-frame" and Frame.is_text(content_type, other_data):
                yield slot, TextFrame.from_wire_v0(frame_id, headers, other_data)
                continue

            if content_type == "cv2-frame" and Frame.is_image(content_type, json):
                yield slot, ImageFrame.from_wire_v0(frame_id, headers, other_data, json, content, content2)
                continue

            if (content_type == "cv2-frame" or content_type == "mlx-frame") and Frame.is_mlx(content_type, content, content2):
                yield slot, MLXFrame.from_wire_v0(frame_id, headers, other_data, content)
                continue

            # v1 element receives v1 frame
            match content_type:
                case "text":
                    yield slot, TextFrame.from_wire_v1(frame_id, headers, other_data, content)
                case "image":
                    yield slot, ImageFrame.from_wire_v1(frame_id, headers, other_data, json, content, content2)
                case "mlx":
                    yield slot, MLXFrame.from_wire_v1(frame_id, headers, other_data, content)

class ElementOutputs(Variables[Output[Any]]):
    """
    Abstract class to be extended with Element Output fields

    Example:
        ```py
        class MyOutputs(ElementOutputs):
            output1 = Output[Frame]()
        ```
    """

    _clients: Dict[str, ElementClient] = {}

    @property
    def has_outputs_with_payloads(self):
        # TODO generically determine which output types can send
        return (
            len(
                [output for output in self.to_dict().values() if output.type is not Preview]
            )
            > 0
        )

    def setup(self, host_by_key: Dict[str, str]):
        if HOST_OUTPUT_KEYS is None:
            return
        output_slots = json.loads(HOST_OUTPUT_KEYS)

        for output in self.to_dict().values():
            output.setup(output_slots, host_by_key)

    def close(self):
        for output in self.to_dict().values():
            output.close()
