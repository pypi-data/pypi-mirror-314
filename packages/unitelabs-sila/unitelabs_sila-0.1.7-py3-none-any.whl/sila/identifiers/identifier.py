from __future__ import annotations

import abc
import dataclasses


@dataclasses.dataclass
class FullyQualifiedIdentifier(abc.ABC):
    """
    A fully qualified identifier uniquely identifies features and their components. Must be universally unique without
    case sensitivity. The string contains only unicode characters up to a maximum of 2048 characters in length.
    """

    @classmethod
    @abc.abstractmethod
    def parse(cls, identifier: str) -> FullyQualifiedIdentifier:
        """
        Initiates a fully qualified identifier based on its string representation.

        Args:
            identifier: The string representation of the fully qualified identifier.

        Returns:
            The fully qualified identifier.

        Raises:
            ValueError: Raised if the provided identifier is malformed.
        """

    def __eq__(self, other: object) -> bool:
        return str(self).lower() == str(other).lower()

    def __hash__(self) -> int:
        return hash(repr(self))
