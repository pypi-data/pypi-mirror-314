from __future__ import annotations

import dataclasses
from collections.abc import Callable
from enum import StrEnum
from typing import Any, Optional, TypeVar, cast

_ClassT = TypeVar("_ClassT")


@dataclasses.dataclass
class _SerialClassData:
    unconverted_keys: set[str] = dataclasses.field(default_factory=set)
    unconverted_values: set[str] = dataclasses.field(default_factory=set)
    to_string_values: set[str] = dataclasses.field(default_factory=set)
    parse_require: set[str] = dataclasses.field(default_factory=set)
    named_type_path: Optional[str] = None
    # Tracks if this data was provided as a decorator to the type.
    # This is used to track "proper types" which are appropriate
    # for serialization and/or dynamic discovery
    from_decorator: bool = False


EMPTY_SERIAL_CLASS_DATA = _SerialClassData()


def serial_class(
    *,
    unconverted_keys: Optional[set[str]] = None,
    unconverted_values: Optional[set[str]] = None,
    to_string_values: Optional[set[str]] = None,
    parse_require: Optional[set[str]] = None,
    named_type_path: Optional[str] = None,
) -> Callable[[_ClassT], _ClassT]:
    """
    An additional decorator to a dataclass that specifies serialization options.

    @param unconverted_keys
        The keys of these items will not be case converted (they will be
        left as-is)
    @param unconverted_values
        The values of these items (referred to by field name) will not undergo
        conversion beyond normal json serialization. They should generally
        contain only json compatible types, otherwise the resulting format is
        undefined.
    @param to_string_values
        For the values of these items (referred to by field name) to be strings.
        This is only useful for types where the string conversion makes sense,
        such as Decimal or int.
    @param parse_require
        This field is always required while parsing, even if it has a default in the definition.
        This allows supporting literal type defaults for Python instantiation, but
        requiring them for the API input.
    @param named_type_path
        The type_spec type-path to this type. This applies only to named types.
    """

    def decorate(orig_class: _ClassT) -> _ClassT:
        cast(Any, orig_class).__unc_serial_data = _SerialClassData(
            unconverted_keys=unconverted_keys or set(),
            unconverted_values=unconverted_values or set(),
            to_string_values=to_string_values or set(),
            parse_require=parse_require or set(),
            named_type_path=named_type_path,
            from_decorator=True,
        )
        return orig_class

    return decorate


class SerialClassDataInspector:
    def __init__(
        self,
        current: _SerialClassData,
    ) -> None:
        self.current = current

    def has_unconverted_key(self, key: str) -> bool:
        return key in self.current.unconverted_keys

    def has_unconverted_value(self, key: str) -> bool:
        return key in self.current.unconverted_values

    def has_to_string_value(self, key: str) -> bool:
        return key in self.current.to_string_values

    def has_parse_require(self, key: str) -> bool:
        return key in self.current.parse_require

    @property
    def from_decorator(self) -> bool:
        return self.current.from_decorator

    @property
    def named_type_path(self) -> Optional[str]:
        return self.current.named_type_path

    @property
    def is_field_proper(self) -> bool:
        return self.current.from_decorator and self.current.named_type_path is not None


def _get_merged_serial_class_data(type_class: type[Any]) -> _SerialClassData | None:
    base_class_data = (
        cast(_SerialClassData, type_class.__unc_serial_data)
        if hasattr(type_class, "__unc_serial_data")
        else None
    )
    if base_class_data is None:
        return None

    if type_class.__bases__ is not None:
        for base in type_class.__bases__:
            curr_base_class_data = _get_merged_serial_class_data(base)
            if curr_base_class_data is not None:
                base_class_data.unconverted_keys |= (
                    curr_base_class_data.unconverted_keys
                )
                base_class_data.unconverted_values |= (
                    curr_base_class_data.unconverted_values
                )
                base_class_data.to_string_values |= (
                    curr_base_class_data.to_string_values
                )
                base_class_data.parse_require |= curr_base_class_data.parse_require
    return base_class_data


def get_serial_class_data(type_class: type[Any]) -> SerialClassDataInspector:
    return SerialClassDataInspector(
        _get_merged_serial_class_data(type_class) or EMPTY_SERIAL_CLASS_DATA
    )


@dataclasses.dataclass(kw_only=True)
class _SerialStringEnumData:
    labels: dict[str, str] = dataclasses.field(default_factory=dict)
    deprecated: set[str] = dataclasses.field(default_factory=set)


def serial_string_enum(
    *, labels: Optional[dict[str, str]] = None, deprecated: Optional[set[str]] = None
) -> Callable[[_ClassT], _ClassT]:
    """
    A decorator for enums to provide serialization data, including labels.
    """

    def decorate(orig_class: _ClassT) -> _ClassT:
        cast(Any, orig_class).__unc_serial_string_enum_data = _SerialStringEnumData(
            labels=labels or {}, deprecated=deprecated or set()
        )
        return orig_class

    return decorate


class SerialStringEnumInspector:
    def __init__(self, current: _SerialStringEnumData) -> None:
        self.current = current

    def get_label(self, value: str) -> Optional[str]:
        return self.current.labels.get(value)

    def get_deprecated(self, value: str) -> bool:
        return value in self.current.deprecated


def get_serial_string_enum_data(type_class: type[StrEnum]) -> SerialStringEnumInspector:
    return SerialStringEnumInspector(
        cast(_SerialStringEnumData, type_class.__unc_serial_string_enum_data)
        if hasattr(type_class, "__unc_serial_string_enum_data")
        else _SerialStringEnumData(),
    )
