import dataclasses
import typing

T = typing.TypeVar("T")


class IdentityHashWrapper(typing.Generic[T]):
    """This allows unhashable types to be used in the SerialUnion, like dict.
    Since we have only one copy of the types themselves, we rely on
    object identity for the hashing."""

    def __init__(self, inner: T) -> None:
        self.inner = inner

    def __hash__(self) -> int:
        return id(self.inner)


@dataclasses.dataclass(kw_only=True, frozen=True, eq=True)
class _SerialUnion:
    """
    This class is to be kept private, to provide flexibility in registration/lookup.
    Places that need the data should access it via help classes/methods.
    """

    # If specified, indicates the Union has a discriminator which should be used to
    # determine which type to parse.
    discriminator: typing.Optional[str] = None
    discriminator_map: typing.Optional[IdentityHashWrapper[dict[str, type]]] = None
    named_type_path: typing.Optional[str] = None


def serial_union_annotation(
    *,
    discriminator: typing.Optional[str] = None,
    discriminator_map: typing.Optional[dict[str, type]] = None,
    named_type_path: typing.Optional[str] = None,
) -> _SerialUnion:
    return _SerialUnion(
        discriminator=discriminator,
        discriminator_map=IdentityHashWrapper(discriminator_map)
        if discriminator_map is not None
        else None,
        named_type_path=named_type_path,
    )


def _get_serial_union(parsed_type: type[T]) -> _SerialUnion | None:
    if not hasattr(parsed_type, "__metadata__"):
        return None
    metadata = parsed_type.__metadata__  # type:ignore[attr-defined]
    if not isinstance(metadata, tuple) or len(metadata) != 1:
        return None
    serial = metadata[0]
    if not isinstance(serial, _SerialUnion):
        return None
    return serial


class SerialClassInspector(typing.Generic[T]):
    def __init__(self, parsed_type: type[T], serial_union: _SerialUnion) -> None:
        self._parsed_type = parsed_type
        self._serial_union = serial_union

    def get_union_underlying(self) -> type[T]:
        return typing.get_args(self._parsed_type)[0]  # type:ignore[no-any-return]

    @property
    def discriminator(self) -> typing.Optional[str]:
        return self._serial_union.discriminator

    @property
    def discriminator_map(self) -> typing.Optional[dict[str, type]]:
        if self._serial_union.discriminator_map is None:
            return None
        return self._serial_union.discriminator_map.inner


def get_serial_union_data(parsed_type: type[T]) -> SerialClassInspector[T] | None:
    serial = _get_serial_union(parsed_type)
    if serial is None:
        return None

    return SerialClassInspector(parsed_type, serial)
