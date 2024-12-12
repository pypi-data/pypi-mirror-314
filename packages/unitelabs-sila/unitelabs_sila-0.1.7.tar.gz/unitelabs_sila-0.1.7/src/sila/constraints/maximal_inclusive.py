import dataclasses
import typing

from sila import datetime

from .constraint import Constraint

T = typing.TypeVar("T", int, float, datetime.date, datetime.time, datetime.datetime)


@dataclasses.dataclass
class MaximalInclusive(Constraint[T]):
    """
    A Maximal Inclusive Constraint specifies the upper bounds for SiLA Numeric Types (the value which is constrained
    must be less than or equal to this Constraint) and SiLA Date Type, SiLA Time Type and SiLA Timestamp Type (the value
    which is constrained must be before or at this Constraint). The Constraint Value must be of the same SiLA Data Type
    as the SiLA Basic Type that this Constraint applies to.
    """

    value: T

    def validate(self, value: T) -> bool:
        if not isinstance(value, type(self.value)):
            raise TypeError()
        if not value <= self.value:
            raise ValueError()

        return True
