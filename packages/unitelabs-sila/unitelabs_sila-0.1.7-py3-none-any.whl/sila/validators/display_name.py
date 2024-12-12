from __future__ import annotations

from .validator import Validator


class DisplayName(Validator[str]):
    """
    Each feature and many of its components (e.g. commands, command parameters, etc.) must have a human readable display
    name. This is the name that will be visible to the user. A display name must be a string of unicode characters of
    maximum 255 characters in length. The display name must be human readable text in American English.
    """

    def __init__(self):
        super().__init__(default="")

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"Display name must be a string of unicode characters, received '{value}'.")

        if not value:
            raise ValueError(f"Display name must not be empty, received '{value}'.")

        if len(value) > 255:
            raise ValueError(f"Display name must not exceed 255 characters in length, received '{value}'.")
