from __future__ import annotations

import abc
import typing

T = typing.TypeVar("T")


class Validator(typing.Generic[T], metaclass=abc.ABCMeta):
    """
    A validator is a descriptor for managed attribute access. Prior to storing any data, it verifies that the new value
    meets various type and range restrictions. If those restrictions aren't met, it raises an exception to prevent data
    corruption at its source.
    """

    def __init__(self, *, default: T):
        self.default = default
        self.name = ""
        self.key = ""

    def __set_name__(self, owner: type, name: str) -> None:
        self.name = owner.__name__
        self.key = f"_{name}"

    def __get__(self, obj: object | None, owner: type) -> T:
        return getattr(obj, self.key, self.default)

    def __set__(self, obj: object | None, value: T) -> None:
        if obj is not None:
            self.validate(value)
            setattr(obj, self.key, value)

    @abc.abstractmethod
    def validate(self, value: T) -> None:
        """
        Custom validators need to inherit from `Validator` and must supply a `validate()` method to test various
        restrictions as needed.

        Args:
            value: The value to validate.

        Raises:
            ValueError: Raised if the value does not comply with the restrictions.
        """
