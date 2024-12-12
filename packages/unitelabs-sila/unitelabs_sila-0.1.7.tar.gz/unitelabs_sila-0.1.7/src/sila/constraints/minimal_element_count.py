import dataclasses

from .constraint import Constraint


@dataclasses.dataclass
class MinimalElementCount(Constraint[list]):
    """
    A Minimal Element Count Constraint specifies the minimum number of elements allowed in a list. The Constraint Value
    must be an integer number equal or greater than zero (0) up to the maximum value of 2⁶³ - 1.
    """

    value: int

    def __post_init__(self):
        if self.value < 0:
            raise ValueError(f"The minimal length value cannot be negative, but {self.value} was provided.")
        if self.value >= 2**63:
            raise ValueError(f"The minimal length value must be less than 2⁶³, but {self.value} was provided.")

    def validate(self, value: list) -> bool:
        if not isinstance(value, list):
            raise TypeError()
        if not len(value) >= self.value:
            raise ValueError()

        return True
