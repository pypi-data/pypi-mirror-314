from __future__ import annotations

import re

from .validator import Validator


class Domain(Validator[str]):
    """
    A domain must consist of one word or words separated by dots ("."). Each word must start with a lower-case letter
    (a-z), followed by any number of lower-case letters (a-z) and digits (0-9). The domain must not exceed 255
    characters in length.
    """

    def __init__(self):
        super().__init__(default="")

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"{self.name} must be a string of unicode characters, received '{value}'.")

        if len(value) > 255:
            raise ValueError(f"{self.name} must not exceed 255 characters in length, received '{value}'.")

        for item in value.split("."):
            if not item or not item[0].islower():
                raise ValueError(f"{self.name} parts must start with a lower-case letter, received '{value}'.")

            if not re.fullmatch(r"[a-z][a-z0-9]*", item):
                raise ValueError(
                    f"{self.name} parts may only contain lower-case letters and digits, received '{value}'."
                )
