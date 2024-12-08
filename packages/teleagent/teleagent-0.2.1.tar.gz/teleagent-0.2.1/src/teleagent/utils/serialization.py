import base64
import typing as tp
import zlib

from telethon.extensions import BinaryReader
from telethon.tl import TLObject

__all__ = ["TelethonString"]


class TelethonString:
    _encoding = "ascii"

    def __init__(self, string: str) -> None:
        self._string = string

    @classmethod
    def from_tl_object(cls, tl_object: TLObject) -> tp.Self:
        return cls(base64.b64encode(zlib.compress(bytes(tl_object))).decode(cls._encoding))

    def to_tl_object(self) -> TLObject:
        return BinaryReader(zlib.decompress(base64.b64decode(self._string))).tgread_object()

    def __str__(self) -> str:
        return self._string
