from __future__ import annotations

import re

from .validator import Validator


class Identifier(Validator[str]):
    """
    An identifier is a name that serves as explicit identifier for different components in SiLA 2. For example, each
    feature and its components (e.g. commands, command parameters, etc.) must be identifiable by an identifier. An
    identifier must be a string of unicode characters, start with an upper-case letter (A-Z) and may be continued by
    lower and upper-case letters (A-Z and a-z) and digits (0-9) up to a maximum of 255 characters in length.
    """

    def __init__(self):
        super().__init__(default="")

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"{self.name} identifier must be a string of unicode characters, received '{value}'.")

        if not value or not value[0].isupper():
            raise ValueError(f"{self.name} identifier must start with an upper-case letter, received '{value}'.")

        if len(value) > 255:
            raise ValueError(f"{self.name} identifier must not exceed 255 characters in length, received '{value}'.")

        if not re.fullmatch(r"[A-Z][a-zA-Z0-9]*", value):
            raise ValueError(f"{self.name} identifier may only contain letters and digits, received '{value}'.")
