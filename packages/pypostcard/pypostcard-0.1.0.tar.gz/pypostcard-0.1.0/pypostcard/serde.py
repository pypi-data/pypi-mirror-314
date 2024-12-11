from dataclasses import fields
from typing import Any, Tuple
from serde.se import Serializer
from serde.de import Deserializer

from .types import serialize, deserialize


class PostcardSerializer(Serializer[str]):
    @classmethod
    def serialize(cls, obj: Any, **opts: Any) -> str:
        serdata = bytearray()
        for field in fields(obj):
            data = serialize(field.type, getattr(obj, field.name))
            if data:
                serdata.extend(data)
        return serdata


class PostcardDeserializer(Deserializer[str]):
    @classmethod
    def deserialize(cls, obj: Any, data: bytes, **opts: Any) -> Tuple[Any, int]:
        retval = {}
        index = 0
        for field in fields(obj):
            val, bytes_used = deserialize(field.type, data[index:])
            index += bytes_used
            if val is not None:
                retval[field.name] = val
        return retval, index


def to_postcard(
    obj: Any,
    se: type[Serializer[str]] = PostcardSerializer,
    **opts: Any,
) -> str:
    """
    Serialize the object into Postcard.

    """
    return se.serialize(
        obj,
        **opts,
    )


def from_postcard(
    c: Any, s: bytes, de: type[Deserializer[bytes]] = PostcardDeserializer, **opts: Any
) -> Any:
    """
    Deserialize from Postcard into the object.
    """
    dict, bytes_used = de.deserialize(c, s, **opts)
    return c(**dict)

def take_from_postcard(
    c: Any, s: bytes, de: type[Deserializer[bytes]] = PostcardDeserializer, **opts: Any
) -> Any:
    """
    Deserialize from Postcard into the object, return the object and number of bytes used.
    """
    dict, bytes_used = de.deserialize(c, s, **opts)
    return c(**dict), bytes_used
