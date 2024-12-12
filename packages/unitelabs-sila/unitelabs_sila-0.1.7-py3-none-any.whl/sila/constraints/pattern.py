import dataclasses
import re

from .constraint import Constraint


@dataclasses.dataclass
class Pattern(Constraint[str]):
    """
    A Pattern Constraint defines the exact sequence of characters that are acceptable, as specified by a so-called
    regular expression. The Constraint Value must be an XML Schema Regular Expression.
    See: https://www.w3.org/TR/xmlschema11-2/#regexs
    """

    value: str

    def validate(self, value: str) -> bool:
        if not isinstance(value, str):
            raise TypeError()
        if not re.fullmatch(self.value, value):
            raise ValueError()

        return True
