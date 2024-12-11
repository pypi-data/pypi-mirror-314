import abc
from enum import Enum
from dataclasses import dataclass, is_dataclass, fields, MISSING

from dataclasses import dataclass, fields
from typing import Callable, Any, Self, get_origin, get_args, Type, Protocol
from .mapping import PrimitiveMapper


@dataclass(frozen=True)
class Value(abc.ABC):
    """Base class for all Value Objects, no other requirements, but it must be a dataclass"""

    def __post_init__(self):
        for field in fields(self):
            value = getattr(self, field.name)
            if get_origin(field.type) is tuple and type(value) is not tuple:
                object.__setattr__(self, field.name, tuple(value))

    @staticmethod
    def _is_nullable(value_cls: Type[Any]) -> bool:
        return (
            get_origin(value_cls) is UnionType
            and len(get_args(value_cls)) == 2
            and get_args(value_cls)[1] is type(None)
        )

    def as_dict(
        self, enum_to_value: bool = True, exclude_defaults: bool = False
    ) -> dict[str, Any]:
        """Convert a dataclass instance to a dictionary, excluding default values."""
        data = PrimitiveMapper.to_primitive(self, enum_to_value, exclude_defaults)
        if type(data) is not dict:
            raise ValueError("Incorrect conversion")
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]):
        return PrimitiveMapper.from_primitive(data, cls)


@dataclass(frozen=True)
class ChangeEvent(Value, abc.ABC):
    """Change of the state of an aggregate"""

    @abc.abstractmethod
    def apply_on(self, aggregate: "Aggregate"):
        """Apply event over aggregate"""


class Aggregate(Protocol):
    """Base of all aggregates under event sourcing approach"""

    @property
    def key(self) -> str:
        """Unique key between same type of aggregate"""

    def add_event_observer(self, callback: Callable[[ChangeEvent, Self], None]):
        """Add a observer of event changes"""

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> Self:
        """Construct the aggregate, not compulsory to implement"""
        raise NotImplementedError()

    def as_dict(self) -> dict[str, Any]:
        """Create a snap, not compulsory to implement"""
        raise NotImplementedError()
