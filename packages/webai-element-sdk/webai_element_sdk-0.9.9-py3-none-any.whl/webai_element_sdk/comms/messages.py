from enum import Enum, auto
from typing import Any, Dict, Mapping
from uuid import UUID, uuid4

import numpy as np
from numpy.typing import NDArray

from msgspec.msgpack import Decoder as Packdecoder

class ColorFormat(Enum):
    """Enumerate image color formats"""

    RGB = auto()
    """Red Green Blue Format"""
    BGR = auto()
    """Blue Green Red Format"""


class Classification:
    """A classification provided by a model or algorithm

    Attributes:
        label (str): The label for the classification
        confidence (float): The confidence in the classification
    """

    def __init__(self, label: str, confidence: float|None):
        """Classification constructor

        Args:
            label: The label for the classification
            confidence: The confidence in the classification
        """
        self.label = label
        self.confidence = confidence

    def to_dict(self) -> Mapping[str, Any]:
        """Provides a dictionary representation of the class instance data

        Returns:
            Class attributes as a dictionary
        """
        return {"label": self.label, "confidence": self.confidence}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Classification":
        """Creates a class instance from a dictionary containing class attributes as keys

        Args:
            data: The dictionary to convert into a class instance

        Returns:
            A class instance
        """
        return cls(data["label"], data["confidence"])


class SegmentationMask:
    """An image segmentation mask

    Attributes:
        binary_mask (NDArray[np.uint8]): The mask in binary form
    """

    def __init__(self, binary_mask: NDArray[np.uint8]):
        """SegmentationMask constructor

        Args:
            binary_mask: The mask in binary form
        """
        self.binary_mask = binary_mask

    def to_dict(self):
        """Provides a dictionary representation of the class instance data

        Returns:
            Class attributes as a dictionary and also includes keys for `height`, `width`, and `dtype` for the mask
        """

        return {
            "binary_mask": self.binary_mask.tobytes(),
            "height": self.binary_mask.shape[0],
            "width": self.binary_mask.shape[1],
            "dtype": str(self.binary_mask.dtype),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SegmentationMask":
        """Creates a class instance from a dictionary containing class attributes as keys

        Args:
            data: The dictionary to convert to class instance

        Returns: A class instance
        """
        npframe = np.frombuffer(data["binary_mask"], dtype=np.dtype(data["dtype"]))

        binary_mask = npframe.reshape((data["height"], data["width"]))

        return cls(binary_mask)


class RegionOfInterest:
    """A region of interest (or bounding box) within an image

    Attributes:
        start_x (int): Minimum x value defining the region boundary
        start_y (int): Minimum y value defining the region boundary
        end_x (int): Maximum x value defining the region boundary
        end_y (int): Maximum y value defining the region boundary
        classes (List[Classification]): The classifications associated with the region
        mask (SegmentationMask): The segmentation mask associated with the region
        id (int): The tracking ID associated with the region
    """

    def __init__(
        self,
        start_x: int,
        start_y: int,
        end_x: int,
        end_y: int,
        classes: list[Classification],
        mask: SegmentationMask | None = None,
        id: int | None = None,
    ):
        """RegionOfInterest constructor

        Args:
            start_x: Minimum x value defining the region boundary
            start_y: Minimum y value defining the region boundary
            end_x: Maximum x value defining the region boundary
            end_y: Maximum y value defining the region boundary
            classes: The classifications associated with the region
            mask: The segmentation mask associated with the region
            id: The tracking ID associated with the region
        """

        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.classes = classes
        self.mask = mask
        self.id = id

    def to_dict(self) -> Mapping[str, Any]:
        """Provides a dictionary representation of the class instance data

        Returns:
            Class attributes as a dictionary
        """
        return {
            "start_x": self.start_x,
            "start_y": self.start_y,
            "end_x": self.end_x,
            "end_y": self.end_y,
            "classes": [cls.to_dict() for cls in self.classes],
            "mask": self.mask.to_dict() if self.mask else None,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RegionOfInterest":
        """Creates a class instance from a dictionary containing class attributes as keys

        Args:
            data: The dictionary to convert to class instance

        Returns: A class instance
        """

        classes = [
            Classification.from_dict(class_data) for class_data in data["classes"]
        ]
        mask = SegmentationMask.from_dict(data["mask"]) if data["mask"] else None
        return cls(
            data["start_x"],
            data["start_y"],
            data["end_x"],
            data["end_y"],
            classes,
            mask,
            data["id"] if "id" in data.keys() and data["id"] else None,
        )


class VariablePayload:
    """Base class for element data types for I/O

    Attributes:
        content_type (str): The type of content captured
    """

    content_type: str


class Frame(VariablePayload):
    """The image data type wrapper for a CV2 NDArray

    Attributes:
        ndframe (NDArray[np.uint8] | None): The image data in CV2 format
        rois (List[RegionOfInterest]): Any regions of interest to be associated with the image
        color_space (ColorFormat): The color format for the image
        headers (Dict[str, Any]): TODO
        frame_id (UUID): The identifier for the image
        other_data (Dict[str, Any]): TODO
        type: str - content type "raw" or None
        content_bytes: bytes - content bytes
    """

    content_type: str = "cv2-frame"

    def __init__(
        self,
        ndframe: NDArray[np.uint8] | None,
        rois: list[RegionOfInterest] = [],
        color_space: ColorFormat = ColorFormat.RGB,
        headers: Dict[str, Any] | None = None,
        frame_id: UUID | None = None,
        other_data: Dict[str, Any] | None = None,
        type: str | None = None,
        content_bytes: bytes | None = None
    ):
        """Frame constructor

        Args:
            ndframe: The image data in CV2 format
            rois: Any regions of interest to be associated with the image
            color_space: The color format for the image
            headers: TODO - doc or deprecate
            frame_id: The identifier for the image
            other_data: TODO - doc or deprecate
            type: str - content type "raw" or None
            content_bytes: bytes - content bytes
        """

        self.content_bytes = content_bytes
        self.ndframe = ndframe
        self.frame_id = frame_id if frame_id is not None else uuid4()
        self.rois = rois
        self.color_space = color_space
        self.headers = headers if headers is not None else dict()
        self.other_data = other_data if other_data is not None else dict()

        if type is not None:
            self.content_type = type

    @staticmethod
    def is_text(content_type, other_data):
        return (content_type == "cv2-frame") and ("message" in other_data)

    @staticmethod
    def is_image(content_type, json):
        return (content_type == "cv2-frame") and ("height" in json) and ("width" in json)

    @staticmethod
    def is_mlx(content_type, content, content2):
        return (content_type == "mlx-frame" or content_type == "cv2-frame") and (len(content) > 0) and (len(content2) == 0)

    @staticmethod
    def as_text(frame_id, headers, other_data, content):
        if 'message' not in other_data: # convert from v1 text frame
            other_data['message'] = content.decode()

        return Frame(
            ndframe=np.zeros(shape=(1, 1, 3), dtype=np.uint8),
            frame_id=frame_id,
            headers=headers,
            other_data=other_data,
        )

    @staticmethod
    def as_image(frame_id, headers, other_data, json, content, content2):
        if len(content2) > 0:
            json["rois"] = Packdecoder().decode(content2)

        npframe = np.frombuffer(content, dtype=np.dtype(json["dtype"]))
        frame = npframe.reshape((json["height"], json["width"], json["channels"]))

        return Frame(
            ndframe=frame,
            rois=[RegionOfInterest.from_dict(roi) for roi in json["rois"]],
            color_space=ColorFormat[json["color_space"]],
            frame_id=frame_id,
            headers=headers,
            other_data=other_data,
        )

    @staticmethod
    def as_mlx(frame_id, headers, other_data, content):
        return Frame(
            ndframe=np.zeros(shape=(1, 1, 3), dtype=np.uint8),
            content_bytes=content,
            frame_id=frame_id,
            headers=headers,
            type="mlx-frame",
            other_data=other_data,
        )

class TextFrame(VariablePayload):
    """The frame type for textual data

    Attributes:
        text (str): The text data as a string
        frame_id (UUID): The identifier for the image
        other_data (Dict[str, Any]): Frame meta data
    """
    content_type: str = "text"

    def __init__(
        self,
        text: str,
        frame_id: UUID | None = None,
        headers: Dict[str, Any] | None = None,
        other_data: Dict[str, Any] | None = None,
    ):
        self.text = text
        self.frame_id = frame_id if frame_id is not None else uuid4()
        self.headers = headers if headers is not None else dict()
        self.other_data = other_data if other_data is not None else dict()

    @staticmethod
    def from_wire_v0(frame_id, headers, other_data):
        return TextFrame(
            text=other_data['message'],
            frame_id=frame_id,
            headers=headers,
            other_data=other_data
        )

    @staticmethod
    def from_wire_v1(frame_id, headers, other_data, content):
        return TextFrame(
            text=content.decode('utf-8'),
            frame_id=frame_id,
            headers=headers,
            other_data=other_data,
        )

class ImageFrame(VariablePayload):
    """The frame type for image data

    Attributes:
    """
    content_type: str = "image"

    def __init__(
        self,
        ndframe: NDArray[np.uint8] | None,
        rois: list[RegionOfInterest] = [],
        color_space: ColorFormat = ColorFormat.RGB,
        headers: Dict[str, Any] | None = None,
        frame_id: UUID | None = None,
        other_data: Dict[str, Any] | None = None,
    ):
        self.ndframe = ndframe
        self.frame_id = frame_id if frame_id is not None else uuid4()
        self.rois = rois
        self.color_space = color_space
        self.headers = headers if headers is not None else dict()
        self.other_data = other_data if other_data is not None else dict()

    @staticmethod
    def from_wire_v0(frame_id, headers, other_data, json, content, content2):
        if len(content2) > 0:
            json["rois"] = Packdecoder().decode(content2)

        npframe = np.frombuffer(content, dtype=np.dtype(json["dtype"]))
        frame = npframe.reshape((json["height"], json["width"], json["channels"]))

        return ImageFrame(
            ndframe=frame,
            rois=[RegionOfInterest.from_dict(roi) for roi in json["rois"]],
            color_space=ColorFormat[json["color_space"]],
            frame_id=frame_id,
            headers=headers,
            other_data=other_data,
        )

    @staticmethod
    def from_wire_v1(frame_id, headers, other_data, json, content, content2):
        return ImageFrame.from_wire_v0(frame_id, headers, other_data, json, content, content2)

class MLXFrame(VariablePayload):
    """The frame type for arbitrary bytes data

    Attributes:
    """
    content_type: str = "mlx"

    def __init__(
        self,
        array: bytes,
        frame_id: UUID | None = None,
        headers: Dict[str, Any] | None = None,
        other_data: Dict[str, Any] | None = None,
    ):
        self.array = array
        self.frame_id = frame_id if frame_id is not None else uuid4()
        self.headers = headers if headers is not None else dict()
        self.other_data = other_data if other_data is not None else dict()

    @staticmethod
    def from_wire_v0(frame_id, headers, other_data, content):
        return MLXFrame(
            array=content,
            frame_id=frame_id,
            headers=headers,
            other_data=other_data,
        )

    @staticmethod
    def from_wire_v1(frame_id, headers, other_data, content):
        return MLXFrame.from_wire_v0(frame_id, headers, other_data, content)

class Preview(VariablePayload):
    """Preview data type"""

    content_type: str = "preview"
