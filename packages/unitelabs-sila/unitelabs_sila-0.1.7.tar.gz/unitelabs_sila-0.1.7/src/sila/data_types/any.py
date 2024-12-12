from __future__ import annotations

import dataclasses
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Any(BasicType[bytes]):
    """
    The SiLA any type represents information that can be of any SiLA Data Type, except for a Custom Data Type (i.e. the
    SiLA any type must not represent information of a custom data type). The value of a SiLA any type must contain both
    the information itself and the SiLA data type.
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA any type."""

        type: typing.Annotated[str, protobuf.Field(1)] = ""
        payload: typing.Annotated[bytes, protobuf.Field(2)] = b""

    def encode(self, value: bytes, field_number: int = 1) -> bytes:
        return b""

    def decode(self, data: bytes) -> bytes:
        return b""

    @classmethod
    def from_native(cls, value: bytes) -> Any.Message:
        raise NotImplementedError()

    @classmethod
    def to_native(cls, message: Any.Message) -> bytes:
        raise NotImplementedError()
