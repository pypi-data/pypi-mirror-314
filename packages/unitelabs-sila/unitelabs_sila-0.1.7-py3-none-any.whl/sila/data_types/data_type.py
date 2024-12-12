from __future__ import annotations

import abc
import dataclasses
import typing

T = typing.TypeVar("T")


@dataclasses.dataclass
class DataType(typing.Generic[T], metaclass=abc.ABCMeta):
    """A SiLA data type describes the data type of any information exchanged between SiLA client and SiLA server."""

    @abc.abstractmethod
    def encode(self, value: T, field_number: int = 1) -> bytes:
        """Serializes a SiLA Data Type into a byte string."""

    @abc.abstractmethod
    def decode(self, data: bytes) -> T:
        """Deserializes a SiLA Data Type from a byte string."""

    def validate(self, value: T) -> None:
        """
        Test various restrictions of the value as needed.

        Args:
            value: The value to validate.

        Raises:
            ValueError: Raised if the value does not comply with the restrictions.
        """
