from __future__ import annotations

import dataclasses
import typing

from .constraint import Constraint

if typing.TYPE_CHECKING:
    from sila import data_types


@dataclasses.dataclass
class AllowedTypes(Constraint[typing.Any]):
    """
    An Allowed Types Constraint defines a list of SiLA Data Types that the SiLA Any Type is allowed to represent. The
    Constraint Value MUST be a list of SiLA Data Types, but MUST NOT be a Custom Data Type or a SiLA Derived Type
    containing a Custom Data Type.
    """

    value: list[data_types.DataType]

    def validate(self, value: typing.Any) -> bool:
        return True
