from __future__ import annotations

import dataclasses
import datetime
import typing

from sila import protobuf

from .basic_type import BasicType
from .timezone import Timezone


@dataclasses.dataclass
class Time(BasicType[datetime.time]):
    """
    The SiLA time type represents an ISO 8601 time (hours [0-23], minutes [0-59], seconds [0-59], milliseconds [0-999],
    with an additional timezone [as an offset from UTC]).
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA time type."""

        hour: typing.Annotated[protobuf.uint, protobuf.Field(3)] = protobuf.uint(0)
        minute: typing.Annotated[protobuf.uint, protobuf.Field(2)] = protobuf.uint(0)
        second: typing.Annotated[protobuf.uint, protobuf.Field(1)] = protobuf.uint(0)
        millisecond: typing.Annotated[protobuf.uint, protobuf.Field(5)] = protobuf.uint(0)
        timezone: typing.Annotated[Timezone.Message, protobuf.Field(4)] = dataclasses.field(
            default_factory=Timezone.Message
        )

    @classmethod
    def from_native(cls, value: datetime.time) -> Time.Message:
        return Time.Message(
            hour=protobuf.uint(value.hour),
            minute=protobuf.uint(value.minute),
            second=protobuf.uint(value.second),
            millisecond=protobuf.uint(int(value.microsecond / 1000)),
            timezone=Timezone.from_native(
                datetime.timezone(offset)
                if value.tzinfo and (offset := value.tzinfo.utcoffset(None))
                else datetime.timezone.utc
            ),
        )

    @classmethod
    def to_native(cls, message: Time.Message) -> datetime.time:
        return datetime.time(
            hour=int(message.hour),
            minute=int(message.minute),
            second=int(message.second),
            microsecond=int(message.millisecond) * 1000,
            tzinfo=Timezone.to_native(message.timezone),
        )
