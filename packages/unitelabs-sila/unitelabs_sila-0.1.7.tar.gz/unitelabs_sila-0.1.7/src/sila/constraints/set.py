import dataclasses
import typing

from sila import datetime

from .constraint import Constraint

T = typing.TypeVar("T", str, int, float, datetime.date, datetime.time, datetime.datetime)


@dataclasses.dataclass
class Set(Constraint[T]):
    """
    A Set Constraint defines a set of acceptable values for a given SiLA Basic Type. The list of acceptable Constraint
    Values must have the same SiLA Data Type as the SiLA Basic Type that this Constraint applies to.
    """

    value: list[T]

    def validate(self, value: T) -> bool:
        if not isinstance(value, type(next(iter(self.value), value))):
            raise TypeError()
        if value not in self.value:
            raise ValueError()

        return True
