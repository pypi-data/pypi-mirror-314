from __future__ import annotations

import dataclasses
import typing

from sila import constraints, protobuf

from .data_type import DataType

T = typing.TypeVar("T")


@dataclasses.dataclass
class Constrained(DataType[T]):
    """
    The SiLA Constrained Type is a SiLA Data Type with one or more Constraints that act as a logical `and`. The SiLA
    Constrained Type must be based on either a SiLA Basic Type or a SiLA List Type. The Constraints in the type itself
    and the type it is based on are to act together as a logical conjunction (and).
    """

    data_type: DataType = dataclasses.field(default_factory=DataType)
    """The SiLA data type of the constrained element."""

    constraints: list[constraints.Constraint] = dataclasses.field(default_factory=list)

    def encode(self, value: T, field_number: int = 1) -> bytes:
        return self.data_type.encode(value, field_number)

    def decode(self, data: bytes) -> T:
        value: T = self.data_type.decode(data)
        self.validate(value)
        return value

    def validate(self, value: T) -> None:
        for constraint in self.constraints:
            try:
                constraint.validate(value)
            except ValueError as value_error:
                raise protobuf.MessageDecodeError(msg=str(value_error))

        super().validate(value)
