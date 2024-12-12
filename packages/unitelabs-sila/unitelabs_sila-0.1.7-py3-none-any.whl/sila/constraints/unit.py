import dataclasses
import enum
import typing

from .constraint import Constraint

T = typing.TypeVar("T", int, float)


class SIUnit(enum.Enum):
    DIMENSIONLESS = "Dimensionless"
    METER = "Meter"
    KILOGRAM = "Kilogram"
    SECOND = "Second"
    AMPERE = "Ampere"
    KELVIN = "Kelvin"
    MOLE = "Mole"
    CANDELA = "Candela"


@dataclasses.dataclass
class UnitComponent:
    unit: SIUnit
    exponent: int = 1


@dataclasses.dataclass
class Unit(Constraint[T]):
    """
    A Unit Constraint specifies the unit of a physical quantity.
    """

    Component: typing.ClassVar = UnitComponent

    SI: typing.ClassVar = SIUnit

    label: str
    """
    The Unit Label is the arbitrary label denoting the physical unit that the Unit Constraint defines. The Unit Label
    must be a string of unicode characters up to a maximum of 255 characters in length.
    """

    components: list[UnitComponent]

    factor: float = 1
    """
    The Conversion Factor specifies the conversion from the unit with a given Unit Label into SI units, according to the
    definition in chapter Unit Conversion.
    """

    offset: float = 0
    """
    The Conversion Offset specifies the conversion from the unit with a given Unit Label into SI units, according to the
    definition in chapter Unit Conversion.
    """

    def __post_init__(self):
        if len(self.label) > 255:
            raise ValueError("The label value must not exceed 255 characters.")

    def validate(self, value: T) -> bool:
        if not isinstance(value, (int, float)):
            raise TypeError()

        return True
