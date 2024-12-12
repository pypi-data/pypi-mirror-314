from __future__ import annotations

import dataclasses
import datetime
import typing

from sila import protobuf

from .basic_type import BasicType
from .timezone import Timezone


@dataclasses.dataclass
class Timestamp(BasicType[datetime.datetime]):
    """
    The SiLA timestamp type represents both, ISO 8601 date and time in one (year [1-9999]), month, day, hours [0-23],
    minutes [0-59], seconds [0-59], milliseconds [0-999], with an additional timezone [as an offset from UTC]).
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA timestamp type."""

        year: typing.Annotated[protobuf.uint, protobuf.Field(6)] = protobuf.uint(0)
        month: typing.Annotated[protobuf.uint, protobuf.Field(5)] = protobuf.uint(0)
        day: typing.Annotated[protobuf.uint, protobuf.Field(4)] = protobuf.uint(0)
        hour: typing.Annotated[protobuf.uint, protobuf.Field(3)] = protobuf.uint(0)
        minute: typing.Annotated[protobuf.uint, protobuf.Field(2)] = protobuf.uint(0)
        second: typing.Annotated[protobuf.uint, protobuf.Field(1)] = protobuf.uint(0)
        millisecond: typing.Annotated[protobuf.uint, protobuf.Field(8)] = protobuf.uint(0)
        timezone: typing.Annotated[Timezone.Message, protobuf.Field(7)] = dataclasses.field(
            default_factory=Timezone.Message
        )

    @classmethod
    def from_native(cls, value: datetime.datetime) -> Timestamp.Message:
        return Timestamp.Message(
            year=protobuf.uint(value.year),
            month=protobuf.uint(value.month),
            day=protobuf.uint(value.day),
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
    def to_native(cls, message: Timestamp.Message) -> datetime.datetime:
        return datetime.datetime(
            year=int(message.year),
            month=int(message.month),
            day=int(message.day),
            hour=int(message.hour),
            minute=int(message.minute),
            second=int(message.second),
            microsecond=int(message.millisecond) * 1000,
            tzinfo=Timezone.to_native(message.timezone),
        )
