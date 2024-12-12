from __future__ import annotations

import dataclasses
import typing

from .constraint import Constraint

T = typing.TypeVar("T", str, bytes)


@dataclasses.dataclass
class Length(Constraint[T]):
    """
    A Length Constraint specifies the exact number of characters allowed. The Constraint Value must be an integer number
    equal or greater than zero (0) up to the maximum value of 2⁶³ - 1.
    """

    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"The length value cannot be negative, but {self.value} was provided.")
        if self.value >= 2**63:
            raise ValueError(f"The length value must be less than 2⁶³, but {self.value} was provided.")

    def validate(self, value: T) -> bool:
        if not isinstance(value, (str, bytes)):
            raise TypeError()
        if not len(value) == self.value:
            raise ValueError()

        return True
