from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from webai_element_sdk.comms.agent import AgentComms
from webai_element_sdk.element.settings import ElementSettings
from webai_element_sdk.element.variables import ElementInputs, ElementOutputs

I = TypeVar("I", bound=ElementInputs | None)
"""Input Type"""

O = TypeVar("O", bound=ElementOutputs | None)
"""Output Type"""

S = TypeVar("S", bound=ElementSettings | None)
"""Settings Type"""


@dataclass
class Context(Generic[I, O, S]):
    """Element context data type

    Attributes:
        inputs (I): Element input context
        outputs (O): Element output context
        settings (S): Element settings context
        logger (AgentComms): The logging instance
        preview_port (Optional[int]): Network port for accessing element preview/visualization data (if any)
    """

    inputs: I
    outputs: O
    settings: S
    logger: AgentComms
    preview_port: Optional[int] = None
