from __future__ import annotations

import enum
import re

from .validator import Validator


class Version(Validator[str]):
    """
    A version consists of up to three numerical parts and a label. "Major", "Minor" and "Patch" version numbers are
    separated by dots. Optionally, an arbitrary text, separated by an underscore MAY be appended,
    e.g. “3.19.373_mighty_lab_devices”.
    """

    class Level(enum.IntEnum):
        """Different levels of specificity of a version. A version is written as "major.minor.patch_label"."""

        MAJOR = 1
        MINOR = 2
        PATCH = 3
        LABEL = 4

    def __init__(self, required: Level, optional: Level | None = None):
        """
        Creates a version validator with a required and optional value, e.g. when the required level is "Minor" and the
        optional level is "Label", a major and minor version are always required and a patch version with an additional
        label can be optionally provided.

        Args:
            required: Up to which level the version parts are required.
            optional: Up to which level the version parts may be optionally required. If none, no parts are optional.
        """
        super().__init__(default="")

        optional = optional or required
        if not required:
            raise ValueError("The required version level must be provided and may not be 'None'.")
        if required.value > optional.value:
            raise ValueError("Optional level can not be less detailed than required level.")

        self.required = required
        self.optional = optional

    def validate(self, value: str):
        if not isinstance(value, str):
            raise ValueError(f"Version must be a string of unicode characters, received '{value}'.")

        if self.optional == Version.Level.LABEL:
            value, _, label = value.partition("_")

            if self.required == Version.Level.LABEL and not label:
                raise ValueError(f"Version must contain a label after an underscore, received '{value}'.")

            if not re.fullmatch(r"[a-zA-Z0-9\_]*", label):
                raise ValueError(f"Version label may only contain letters, digits and underscores, received '{value}'.")

        parts = value.split(".")
        if len(parts) < min(self.required.value, Version.Level.PATCH):
            raise ValueError(
                f"Version must contain at least {self.required.value} parts separated by dots, received '{value}'."
            )

        if len(parts) > min(self.optional.value, Version.Level.PATCH):
            raise ValueError(
                f"Version must contain at most {self.optional.value} parts separated by dots, received '{value}'."
            )

        for item in parts:
            if not item.isdigit():
                raise ValueError(f"Version parts must represent a numeric value, received '{value}'.")
