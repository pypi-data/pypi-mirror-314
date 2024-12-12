import abc
import typing

T = typing.TypeVar("T")


class Constraint(typing.Generic[T], metaclass=abc.ABCMeta):
    """
    A Constraint limits the allowed value, size, range, etc. that a SiLA Data Type can assume. A SiLA Server must check
    all Constraints and issue a Validation Error if Constraints are violated.
    """

    @abc.abstractmethod
    def validate(self, value: T) -> bool:
        """Return True if the given value is valid, raises a ValueError otherwise"""
