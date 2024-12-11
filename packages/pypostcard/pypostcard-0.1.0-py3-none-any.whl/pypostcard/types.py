from typing import Any, Generic, Tuple, TypeVar, Union
import enum
import logging
import struct

T = TypeVar("T")
N = TypeVar("N", bound=int)
E = TypeVar("E", bound=enum.Enum)

_LOG = logging.getLogger(__name__)


def serialize(type_hint, value) -> bytes:
    if hasattr(type_hint, "serialize"):
        return value.serialize(type_hint)
    if issubclass(type_hint, bool):
        return bytes([int(value)])
    _LOG.warning("Unsupported type: %s", type_hint)
    return b""


def deserialize(type_hint, data: bytes) -> Tuple[Union[Any, None], int]:
    if hasattr(type_hint, "deserialize"):
        return type_hint.deserialize(type_hint, data)
    if issubclass(type_hint, bool):
        return True if data[0] == 1 else False, 1
    raise TypeError(f"Unsupported type: {type_hint}")
    _LOG.warning("Unsupported type: %s", type_hint)
    return None, 0


class u8(int):
    def serialize(self, hint):
        return self.to_bytes(1, "little", signed=False)

    @staticmethod
    def deserialize(hint: Any, data: bytes):
        return u8(int.from_bytes(data[0:1], "little", signed=False)), 1


class i8(int):
    def serialize(self, hint):
        return self.to_bytes(1, "little", signed=True)

    @staticmethod
    def deserialize(hint: Any, data: bytes):
        return i8(int.from_bytes(data[0:1], "little", signed=True)), 1


class varint(int):
    def serialize(self, hint):
        value = int(self)  # Copy
        if self.SIGNED:
            value = abs(value) << 1
            if self < 0:
                value = (value - 1) | 1
        retval = bytearray()
        while True:
            data = value & 0x7F
            value = value >> 7
            if value > 0:
                retval.append(data | 0x80)
            else:
                retval.append(data)
                break
        return retval

    @staticmethod
    def deserialize(hint: Any, data: bytes):
        retval = 0
        bytes_used = 0
        for i, byte in enumerate(data):
            retval = retval | ((byte & 0x7F) << (i * 7))
            bytes_used += 1
            if byte & 0x80 == 0:
                break
        if hint.SIGNED:
            if retval & 1:
                retval = -((retval >> 1) + 1)
            else:
                retval = retval >> 1

        return hint(retval), bytes_used


class u16(varint):
    SIZE = 2
    SIGNED = False


class i16(varint):
    SIZE = 2
    SIGNED = True


class u32(varint):
    SIZE = 4
    SIGNED = False


class i32(varint):
    SIZE = 4
    SIGNED = True


class u64(varint):
    SIZE = 8
    SIGNED = False


class i64(varint):
    SIZE = 8
    SIGNED = True


class u128(varint):
    SIZE = 16
    SIGNED = False


class i128(varint):
    SIZE = 16
    SIGNED = True


class f32(float):
    def serialize(self, hint):
        return struct.pack("<f", self)

    @staticmethod
    def deserialize(hint: Any, data: bytes):
        return f32(struct.unpack("<f", data[0:4])[0]), 4


class f64(float):
    def serialize(self, hint):
        return struct.pack("<d", self)

    @staticmethod
    def deserialize(hint: Any, data: bytes):
        return f64(struct.unpack("<d", data[0:8])[0]), 8


class Enum(Generic[T, E]):
    def __init__(self, *args) -> None:
        super().__init__()
        self._value: enum.Enum = args[0]

    @staticmethod
    def deserialize(hint: Any, data: bytes):
        type_hint, enum_type = hint.__args__
        # print("Deserializing enum", type_hint, enum_type)
        value, bytes_used = deserialize(type_hint, data)
        return Enum(enum_type(value)), bytes_used

    def serialize(self, hint: Any) -> bytes:
        type_hint, _ = hint.__args__
        return serialize(type_hint, type_hint(self._value.value))

    def __repr__(self) -> str:
        return repr(self._value)

    def __eq__(self, value: object) -> bool:
        return self._value == value


class List(Generic[T, N]):
    def __init__(self, *args) -> None:
        super().__init__()
        if len(args) == 1 and isinstance(args[0], list):
            self._list = args[0]
        else:
            self._list = [*args]

    @staticmethod
    def deserialize(hint: Any, data: bytes) -> list[T, N]:
        type_hint, size = hint.__args__
        index = 0
        retval = []
        for i in range(size):
            value, bytes_used = deserialize(type_hint, data[index:])
            if value is None:
                break
            index += bytes_used
            retval.append(value)
        return List(retval), index

    def serialize(self, hint: Any) -> bytes:
        type_hint, size = hint.__args__
        assert size == len(self._list)
        retval = bytearray()
        for value in self._list:
            v = serialize(type_hint, type_hint(value))
            retval.extend(v)
        return retval

    def __len__(self) -> int:
        return len(self._list)

    def __getitem__(self, key: int) -> T:
        return self._list[key]

    def __repr__(self) -> str:
        return f"List{repr(self._list)}"

    def __eq__(self, value: object) -> bool:
        if isinstance(value, List):
            return self._list == value._list
        return self._list.__eq__(value)
