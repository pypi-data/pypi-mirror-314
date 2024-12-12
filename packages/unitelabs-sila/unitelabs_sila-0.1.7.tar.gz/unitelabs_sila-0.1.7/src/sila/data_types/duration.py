from __future__ import annotations

import dataclasses
import datetime
import typing

from sila import protobuf

from .basic_type import BasicType


@dataclasses.dataclass
class Duration(BasicType[datetime.timedelta]):
    """
    The SiLA duration type represents a signed, fixed-length span of time represented as a count of seconds and
    fractions of seconds at nanosecond resolution. It is independent of any calendar and concepts like "day" or "month".
    """

    @dataclasses.dataclass
    class Message(protobuf.BaseMessage):
        """Schema for the SiLA duration type."""

        seconds: typing.Annotated[int, protobuf.Field(1)] = 0
        nanos: typing.Annotated[int, protobuf.Field(2)] = 0

    @classmethod
    def from_native(cls, value: datetime.timedelta) -> Duration.Message:
        seconds, rest = divmod(value.total_seconds(), 1)

        return Duration.Message(seconds=int(seconds), nanos=int(rest * 1e9))

    @classmethod
    def to_native(cls, message: Duration.Message) -> datetime.timedelta:
        return datetime.timedelta(seconds=int(message.seconds), microseconds=int(message.nanos / 1000))
