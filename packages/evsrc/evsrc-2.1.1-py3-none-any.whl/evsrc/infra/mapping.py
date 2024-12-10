"""Map Value objects to dict and construct them"""

from enum import Enum
from dataclasses import MISSING, fields, is_dataclass
from typing import Any, Protocol, Self, Type, TypeVar, get_args, get_origin
from types import UnionType

from ..model import Value

T = TypeVar("T", bound=Value)


class DictMapper(Protocol):
    @classmethod
    def to_dict(cls, value: Value) -> dict[str, Any]:
        """Convert to dict of basic primitives, jsonable"""
        ...

    @classmethod
    def from_dict(cls, value_cls: Type[T], data: dict[str, Any]) -> T:
        """Construct object from primitive dict"""
        ...


class ValueDictMapper(DictMapper):
    """Parse Value objects to plain dictionaries and construct from them"""

    _mappers = {}

    @classmethod
    def add_mapper(cls, mapper: Type[DictMapper], value_cls: Type[Value]):
        """Add customized mapper to especific value class"""
        cls._mappers[value_cls] = mapper

    @classmethod
    def to_dict(
        cls, value: Value, enum_as_value: bool = True, ommit_defaults: bool = True
    ) -> dict[str, Any]:
        """Convert a Value object to a jsonable dict"""
        for value_cls, mapper in cls._mappers.items():
            if type(value) is value_cls:
                return mapper.to_dict(value)

        result = {}
        for field in fields(value):
            value_ = getattr(value, field.name)
            if value_ != field.default and (
                field.default_factory is MISSING or value_ != field.default_factory()
            ):
                result[field.name] = cls._as_primitive(
                    value_, enum_as_value, ommit_defaults
                )
        return result

    @classmethod
    def from_dict(cls, value_cls: Type[T], data: dict[str, Any]) -> T:
        """Construct a Value object from a primitive dict"""
        for mapper_cls, mapper in cls._mappers.items():
            if value_cls == mapper_cls:
                return mapper.from_dict(value_cls, data)

        init_values = {}
        for field in fields(value_cls):
            if field.name in data:
                init_values[field.name] = cls._convert_to_value(
                    field.type, data[field.name]
                )
            else:
                if field.default is not MISSING:
                    init_values[field.name] = field.default
                elif field.default_factory is not MISSING:  # Handle default_factory
                    init_values[field.name] = field.default_factory()
                else:
                    raise ValueError(
                        f"Field {field.name} is missing and has no default value."
                    )

        return value_cls(**init_values)

    @staticmethod
    def _is_nullable(value_cls: Type[Any]) -> bool:
        return (
            get_origin(value_cls) is UnionType
            and len(get_args(value_cls)) == 2
            and get_args(value_cls)[1] is type(None)
        )

    @classmethod
    def _as_primitive(cls, value, enum_as_value, ommit_defaults):
        if is_dataclass(value.__class__):
            # If the value is another dataclass, recursively convert to dict
            return ValueDictMapper.to_dict(value, enum_as_value, ommit_defaults)
        elif isinstance(value, Enum):
            if enum_as_value:
                return value.value
            else:
                return value.name
        elif isinstance(value, list):
            return [
                cls._as_primitive(item, enum_as_value, ommit_defaults) for item in value
            ]
        elif isinstance(value, tuple):
            return tuple(
                [
                    cls._as_primitive(item, enum_as_value, ommit_defaults)
                    for item in value
                ]
            )
        elif isinstance(value, dict):
            return {
                key: cls._as_primitive(val, enum_as_value, ommit_defaults)
                for key, val in value.items()
            }

        return value

    @classmethod
    def _convert_to_value(cls, value_cls, value):
        if get_origin(value_cls) is None and issubclass(value_cls, Value):
            return ValueDictMapper.from_dict(value_cls, value)
        elif get_origin(value_cls) is list:
            return [
                cls._convert_to_value(get_args(value_cls)[0], item) for item in value
            ]
        elif get_origin(value_cls) is tuple:
            return tuple(
                [cls._convert_to_value(get_args(value_cls)[0], item) for item in value]
            )
        elif get_origin(value_cls) is dict and get_args(value_cls)[0] is str:
            return {
                key: cls._convert_to_value(get_args(value_cls)[1], val)
                for key, val in value.items()
            }
        elif get_origin(value_cls) is None and issubclass(value_cls, Enum):
            if type(value) is str:
                return value_cls[value]
            else:
                return value_cls(value)
        elif cls._is_nullable(value_cls):
            if value is None:
                return
            return cls._convert_to_value(get_args(value_cls)[0], value)

        return value
