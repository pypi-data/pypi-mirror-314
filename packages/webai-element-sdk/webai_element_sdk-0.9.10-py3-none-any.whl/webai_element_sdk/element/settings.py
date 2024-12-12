from abc import ABC
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, cast, get_args, Union
from warnings import warn

from webai_element_sdk.comms.utils import load_config
from typing_extensions import NotRequired, TypedDict

T = TypeVar("T")
N = TypeVar("N", int, float)
"""Numeric Type"""


class DependencyType(str, Enum):
    AND = "and"
    OR = "or"
    NOT_EQUALS = "not_equals"
    EQUALS = "equals"


@dataclass
class DependencyCondition:
    type: DependencyType
    setting: Optional[str] = None
    value: Any = None
    conditions: List['DependencyCondition'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        if self.type == DependencyType.EQUALS or self.type == DependencyType.NOT_EQUALS:
            return {
                "type": self.type.value,
                "setting": self.setting,
                "value": self.value
            }
        else:
            return {
                "type": self.type.value,
                "conditions": [cond.to_dict() for cond in self.conditions]
            }


# Helper functions to create dependencies
def equals(setting: str, value: Any) -> DependencyCondition:
    return DependencyCondition(type=DependencyType.EQUALS, setting=setting, value=value)


def not_equals(setting: str, value: Any) -> DependencyCondition:
    return DependencyCondition(type=DependencyType.NOT_EQUALS, setting=setting, value=value)


def and_condition(*conditions: DependencyCondition) -> DependencyCondition:
    return DependencyCondition(type=DependencyType.AND, conditions=list(conditions))


def or_condition(*conditions: DependencyCondition) -> DependencyCondition:
    return DependencyCondition(type=DependencyType.OR, conditions=list(conditions))


@dataclass
class Setting(Generic[T]):
    """An abstract parent class used for element setting classes.

    Attributes:
        name: The name of the setting.
        default: The default value of the setting.
        display_name: The display name of the setting.
        description: The description of the setting.
        type: The setting value type.
        value: This is a property that returns the element setting value, if valid.
        required: Whether this setting requires a value in order to run
        sensitive: Whether this setting value contains information that should not be exposed outside of the application
    """

    name: str
    default: T
    display_name: Optional[str] = None
    description: Optional[str] = None
    hints: Optional[List[str]] = None
    valid_values: Optional[List[T]] = None
    strip_whitespace: Optional[bool] = True
    required: Optional[bool] = True
    sensitive: Optional[bool] = False
    depends_on: Optional[DependencyCondition] = None
    config_key: int = 0,
    refreshable: bool = False

    @property
    def type(self) -> Type[T]:
        if "__orig_class__" in self.__dict__:
            return get_args(self.__orig_class__)[0]  # type: ignore
        return get_args(self.__orig_bases__[0])[0]  # type: ignore

    @property
    def extra_fields(self) -> Dict[str, Any]:
        return {}

    @cached_property
    def value(self) -> T:
        """Returns the element setting value, if valid."""

        raw_settings: Dict[str, Any] = load_config(self.config_key)

        # TODO: determine if we should add a default type coercion option
        setting_value: T = cast(T, raw_settings.get(self.name))

        if setting_value is None:
            setting_value = self.default

        if self.strip_whitespace and type(setting_value) == str:
            setting_value = setting_value.strip()

        if self.type in [int, float]:  # type: ignore
            setting_value = self.type(setting_value)

        # Validate retrieved setting type
        if type(setting_value) != self.type:
            raise ValueError(
                f"Setting value retrieval failed for '{self.name}'. "
                + f"Setting value was the wrong type. "
                + f"Expected: {self.type} Got: {type(setting_value)} "
            )

        if self.valid_values is not None:
            if setting_value not in self.valid_values:
                raise ValueError(
                    f"For setting {self.name}, setting value of "
                    + f"{setting_value} was not in {self.valid_values}"
                )

        return setting_value

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "default": self.default,
            "type": self.type.__name__,
            "hints": self.hints,
            "validValues": self.valid_values,
            "required": self.required,
            "sensitive": self.sensitive,
            "refreshable": self.refreshable,
            "dependsOn": self.depends_on.to_dict() if self.depends_on else None,
            **self.extra_fields,
        }

    def reset_values(self):
        self.__dict__.pop("value", None)
        self.config_key = self.config_key + 1


class ElementSettings(ABC):
    @classmethod
    def to_list(cls) -> List[Dict[str, Any]]:
        settings: List[Setting[Any]] = []
        setting_names: List[str] = []
        for setting in vars(cls).values():
            if isinstance(setting, Setting):
                settings.append(setting)  # type: ignore
                setting_names.append(setting.name)

        for setting in settings:
            if setting.depends_on:
                check_settings_deps_exist(setting.depends_on, setting_names)

        return [setting.to_dict() for setting in settings]

    @classmethod
    def reset_values(cls):
        for setting in vars(cls).values():
            if isinstance(setting, Setting):
                setting.reset_values()


def check_settings_deps_exist(dep_cond: DependencyCondition, setting_names: List[str]):
    if dep_cond.type == DependencyType.EQUALS:
        if dep_cond.setting not in setting_names:
            raise RuntimeError(f"Setting name: {dep_cond.setting} is not defined for element")
    else:
        for cond in dep_cond.conditions:
            check_settings_deps_exist(cond, setting_names)


@dataclass
class NumberSetting(Setting[N]):
    """A setting that holds either an int or float value

    Attributes:
        min_value: The mininum numeric value allowed for the setting
        max_value: The maximum numeric value allowed for the setting
        step: The step size (graduations) the setting should take on
    """

    min_value: Optional[N] = None
    max_value: Optional[N] = None
    step: Optional[N] = None

    @property
    def extra_fields(self) -> Dict[str, Any]:
        return {
            "minValue": self.min_value,
            "maxValue": self.max_value,
            "step": self.step,
        }


@dataclass
class TextSetting(Setting[str]):
    """Setting that holds a string value

    Attributes:
        character_limit: Character length limit for the setting
    """

    character_limit: Optional[int] = None

    @property
    def extra_fields(self) -> Dict[str, Any]:
        return {
            "characterLimit": self.character_limit,
        }


@dataclass
class BoolSetting(Setting[bool]):
    """Setting that holds a boolean value"""

    required: Optional[bool] = False


class ArtifactSettingParams(TypedDict):
    name: NotRequired[str]
    display_name: NotRequired[str]
    required: NotRequired[bool]
    depends_on: NotRequired['DependencyCondition']


def generate_artifact_setting(settings_or_required: Union[ArtifactSettingParams, bool] = None):
    if isinstance(settings_or_required, bool):
        # If you are changing a caller of this function please refactor the callar to pass in a dict, not a bool
        # Passing in a bool is deprecated and will be removed in a future version
        warn('Calling generate_artifact_setting with a boolean is deprecated', DeprecationWarning, stacklevel=2)
        settings = {
            'required': settings_or_required
        }
    elif settings_or_required is None:
        settings = {}
    else:
        settings = settings_or_required

    return TextSetting(
        name=settings.get('name', "artifactId"),
        display_name=settings.get('display_name', "Trained Artifact"),
        required=settings.get('required', True),
        default="",
        hints=["artifact"],
    )


class ApiKeySettingParams(TypedDict):
    name: str
    display_name: str
    required: NotRequired[bool]
    depends_on: NotRequired['DependencyCondition']


def generate_api_key_setting(settings: ApiKeySettingParams):
    return TextSetting(
        name=settings.get('name'),
        display_name=settings.get('display_name'),
        required=settings.get("required", True),
        depends_on=settings.get("depends_on", None),
        default="",
        sensitive=True,
        hints=["api_key"],
    )
