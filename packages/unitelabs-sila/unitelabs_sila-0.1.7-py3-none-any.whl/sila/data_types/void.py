from __future__ import annotations

import dataclasses

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Void(BasicType[None]):
    """The SiLA void type represents no data. It must only be used as a value of the SiLA any type."""

    def encode(self, value: None, field_number: int = 1) -> bytes:
        return b""

    def decode(self, data: bytes) -> None:
        return None

    @classmethod
    def from_native(cls, value: None) -> protobuf.BaseMessage:
        raise NotImplementedError()

    @classmethod
    def to_native(cls, message: protobuf.BaseMessage) -> None:
        raise NotImplementedError()
