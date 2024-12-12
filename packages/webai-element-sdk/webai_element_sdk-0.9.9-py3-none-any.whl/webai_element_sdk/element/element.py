import asyncio
import logging
import os
import uuid
from collections.abc import AsyncIterator
from functools import wraps
from typing import Any, Callable, Coroutine, Dict, List, Optional, get_origin

import traceback
import semver

from webai_element_sdk.comms import AgentComms
from webai_element_sdk.comms.utils import async_noop
from webai_element_sdk.element.context import Context
from webai_element_sdk.element.settings import ElementSettings
from webai_element_sdk.element.utils import check_server_status_until_success_or_timeout
from webai_element_sdk.element.variables import ElementInputs, ElementOutputs

PREVIEW_PORT = os.getenv("PREVIEW_PORT")

logger = logging.getLogger(__name__)


class Element:
    """Class used to instantiate an element

    Attributes:
        id (UUID): The element identifier
        name (str): The name of the element
        version (Optional[str]): The semantic version of the element
        display_name (Optional[str]): The name of the element to use for UI display purposes
        settings (Optional[ElementSettings]): The element settings attributed to the element
        inputs (Optional[ElementInputs]): The inputs to be operated upon by the element
        outputs (Optional[ElementOutputs]): The outputs provided by the element for downstream consumption
        packages (Optional[List[str]]): TODO
        is_training (Optional[bool]): Does this element perform traditional ML training functions?
        is_inference (Optional[bool]): Does this element perform traditional ML inference functions?
        sub_elements (Optional[List["Element"]]): TODO
        parent_element_id (Optional[str]): TODO
        description (Optional[str]): A short, user facing description of what the element does
        agent_comms (AgentComms): The runtime agent communication instance
        startup_func (Coroutine[Any, Any, None]): The function registered via decorator to be executed at element startup
        executor_func (Coroutine[Any, Any, None]): The function registered via decorator to be executed continuously as the element's main process
        shutdown_func (Coroutine[Any, Any, None]): The function registered via decorator to be executed at element shutdown or termination
        ctx (Context): The context object providing element detail/state at execution time
    """

    def __init__(
        self,
        id: uuid.UUID,
        name: str,
        version: Optional[str] = None,
        framework_version: Optional[str] = None,
        display_name: Optional[str] = None,
        settings: Optional[ElementSettings] = None,
        inputs: Optional[ElementInputs] = None,
        outputs: Optional[ElementOutputs] = None,
        packages: Optional[List[str]] = [],
        is_training: Optional[bool] = False,
        is_inference: Optional[bool] = False,
        sub_elements: Optional[List["Element"]] = [],
        parent_element_id: Optional[str] = "",
        training_metrics_schema: Optional[Dict[str, Any]] = None,
        metrics_schema: Optional[Dict[str, Any]] = None,
        description: Optional[str] = None,
    ):
        """Element constructor

        Args:
            id: The element identifier
            name: The name of the element
            version: The semantic version of the element
            framework_version: The "major.minor" version of the framework used to build this element
            display_name: The name of the element to use for UI display purposes
            settings: The element settings attributed to the element
            inputs: The inputs to be operated upon by the element
            outputs: The outputs provided by the element for downstream consumption
            packages: TODO
            is_training: Does this element perform traditional ML training functions?
            is_inference: Does this element perform traditional ML inference functions?
            sub_elements: TODO
            parent_element_id: TODO
            training_metrics_schema: Schema used to define charts for run history
            metrics_schema: Schema used to define charts for run history
            description: A short, user facing description of what the element does

        Raises:
            BaseException: `name` argument cannot be empty
            BaseException: `version` argument must use semantic versioning
        """
        assert len(name.strip()) > 0, "Name cannot be empty"
        if version:
            assert semver.Version.is_valid(version), "Must use semantic versioning"

        self.id = id
        self.name = name
        self.display_name = display_name or name
        self.version = version
        self.framework_version = framework_version
        self.settings = settings
        self.inputs = inputs
        self.outputs = outputs
        self.packages = packages
        self.is_training = is_training
        self.is_inference = is_inference
        self.description = description

        self.sub_elements = sub_elements
        self.parent_element_id = parent_element_id

        assert not (
            training_metrics_schema is not None and metrics_schema is not None
        ), "Either training_metrics_schema or metrics_schema can be set, not both"
        self.training_metrics_schema = training_metrics_schema
        self.metrics_schema = metrics_schema

        self.agent_comms = AgentComms()

        self.startup_func = async_noop
        self.executor_func = async_noop
        self.refresh_func = async_noop
        self.shutdown_func = async_noop

        self.ctx = self._build_context()

    async def _setup_inputs(self):
        if self.inputs:
            self.inputs.setup(self._teardown)

    async def _setup_outputs(self, host_by_key):
        if self.outputs:
            self.outputs.setup(host_by_key)

    async def _setup(self):
        self.agent_comms.setup()

    async def _ready(self):
        self.agent_comms.ready()
        return self.agent_comms.wait_until_begin()

    async def _setup_training_metrics(self):
        if self.training_metrics_schema is not None:
            logger.warning(
                "training_metrics_schema is deprecated and will be removed. Use metrics_schema."
            )
            self.agent_comms.init_training_metrics(self.training_metrics_schema)

    async def _setup_metrics(self):
        if self.metrics_schema is not None:
            self.agent_comms.init_training_metrics(self.metrics_schema)

    async def _do_refresh_settings(self):
        if self.settings is not None:
            self.settings.reset_values()
        await self.refresh_func(self.ctx)

    async def _open_preview(self):
        if PREVIEW_PORT:
            await check_server_status_until_success_or_timeout(
                f"http://localhost:{PREVIEW_PORT}"
            )
            self.agent_comms.open(PREVIEW_PORT)

    def _teardown(self):
        self.agent_comms.complete()
        self.agent_comms.shutdown()

        if self.outputs:
            self.outputs.close()

    def _build_context(self):
        return Context[
            ElementInputs | None, ElementOutputs | None, ElementSettings | None
        ](
            inputs=self.inputs,
            outputs=self.outputs,
            settings=self.settings,
            logger=self.agent_comms,
            preview_port=int(PREVIEW_PORT) if PREVIEW_PORT else None,
        )

    def startup(self, func: Callable[[Any], Coroutine[Any, Any, Any]]):
        """Decorator to be used to define behavior that should execute ahead of the general element process execution"""

        @wraps(func)
        async def wrapper():
            self.agent_comms.startup()
            await func(self.ctx)

        self.startup_func = wrapper
        return wrapper

    def refresh(self, func: Callable[
                [Context[ElementInputs | None, ElementOutputs | None, ElementSettings | None]],
                None
        ]):
        """Decorator to be used to define behavior that should execute when element settings are refreshed"""

        self.refresh_func = func
        return async_noop

    def executor(
        self,
        func: Optional[
            Callable[
                [Context[ElementInputs | None, ElementOutputs | None, ElementSettings | None]],
                AsyncIterator[Any],
            ]
        ] = None,
    ):
        """Decorator to be used to define ongoing element process execution"""

        def decorator(
            f: Callable[
                [Context[ElementInputs | None, ElementOutputs | None, ElementSettings | None]],
                AsyncIterator[Any],
            ]
        ):
            async def execute_f():
                if self.outputs and self.outputs.has_outputs_with_payloads:
                    async for outputs in f(self.ctx):
                        if outputs is not None:
                            if any(map(lambda x: isinstance(x, tuple), outputs)):
                                await asyncio.gather(
                                    *[
                                        output[0].send(output[1])
                                        for output in outputs
                                        if output is not None
                                    ]
                                )
                            else:
                                output, value = outputs
                                await output.send(value)
                else:
                    await f(self.ctx) # type: ignore

            @wraps(f)
            async def wrapper():
                if self.inputs:
                    await self.inputs.receive(execute_f)
                else:
                    await execute_f()

            self.executor_func = wrapper
            return wrapper

        if func:
            return decorator(func)
        return decorator

    def shutdown(self, func: Callable[[Any], Coroutine[Any, Any, Any]]):
        """Decorator to be used to define behavior that should execute after general element process execution (i.e., at shutdown or termination of the process)"""

        @wraps(func)
        async def wrapper():
            await func(self.ctx)

        self.shutdown_func = wrapper
        return wrapper

    async def run(self):
        try:
            await self._setup()
            await self._setup_inputs()

            await self.startup_func()

            (host_by_key) = await self._ready()
            await self._setup_outputs(host_by_key)
            await self._setup_training_metrics()
            await self._setup_metrics()

            await asyncio.gather(
                self.agent_comms.wait_for_refresh(self._do_refresh_settings),
                self.executor_func(),
                self._open_preview(),
            )
        except Exception as ex:
            self.agent_comms.exception(ex, traceback.format_exc())
            traceback.print_exc()
            raise ex
        finally:
            await self.shutdown_func()
            self._teardown()

    def generate_metadata(self):
        inputs: List[Dict[str, str]] = []
        if self.inputs:
            for name, input in self.inputs.to_dict().items():
                if get_origin(input.type) == AsyncIterator:
                    content_type = input.type.__args__[0].content_type
                else:
                    content_type = input.type.content_type

                inputs.append(
                    {
                        "name": name,
                        "contentType": content_type,
                    }
                )

        outputs: List[Dict[str, str]] = []
        if self.outputs:
            for name, value in self.outputs.to_dict().items():
                outputs.append(
                    {
                        "name": name,
                        "contentType": value.type.content_type,
                    }
                )

        settings: List[Dict[str, str]] = []
        if self.settings:
            settings = list(self.settings.to_list())

        sub_elements: List[Dict[str, Any]] = []
        if self.sub_elements:
            for sub_element in self.sub_elements:
                metadata = sub_element.generate_metadata()
                metadata["parentElementId"] = str(self.id)
                metadata["name"] = f'{self.name}.{metadata["name"]}'
                metadata["version"] = self.version
                metadata["frameworkVersion"] = self.framework_version
                del metadata["subElements"]
                # TODO: determine if/how to handle common settings, inputs, outputs
                sub_elements.append(metadata)

        return {
            "id": str(self.id),
            "name": self.name,
            "displayName": self.display_name,
            "version": self.version,
            "frameworkVersion": self.framework_version,
            "inputs": inputs,
            "outputs": outputs,
            "settings": settings,
            "packages": self.packages,
            "isTraining": self.is_training,
            "isInference": self.is_inference,
            "subElements": sub_elements,
            "parentElementId": "",
            "description": self.description
        }
