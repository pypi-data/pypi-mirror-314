from __future__ import annotations

import re
import uuid

from .validator import Validator


class UUID(Validator[str]):
    """
    A UUID is a Universally Unique IDentifier according to RFC 4122. SiLA always uses the UUID in its string
    representation (e.g. “f81d4fae-7dec-11d0-a765-00a0c91e6bf6”), as specified by the formal definition of the UUID
    string representation in RFC 4122. It is recommended to always use lower case letters (a-f). In any case,
    comparisons of UUIDs in their string representation must always be performed ignoring lower and upper case,
    i.e. “a” = “A”, “b” = “B”, ... , “f” = “F”.
    """

    def __init__(self):
        super().__init__(default=str(uuid.uuid4()))

    def validate(self, value: str) -> None:
        if not isinstance(value, str):
            raise ValueError(f"UUID must be a string of unicode characters, received '{value}'.")

        if not re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}", value):
            raise ValueError(f"UUID may only contain letters and digits, received '{value}'.")
