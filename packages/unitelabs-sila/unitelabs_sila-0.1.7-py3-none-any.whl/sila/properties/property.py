from __future__ import annotations

import abc
import dataclasses

from sila import core, data_types, identifiers


@dataclasses.dataclass
class Property(core.Handler, metaclass=abc.ABCMeta):
    """A property describes certain aspects of a SiLA server that do not require an action on the SiLA server."""

    data_type: dataclasses.InitVar[data_types.DataType] = data_types.Void()
    """The SiLA data type of the property."""

    message: data_types.Structure = dataclasses.field(init=False, repr=False)

    def __post_init__(self, data_type: data_types.DataType):
        self.message = data_types.Structure(
            elements=[
                data_types.Structure.Element(
                    identifier=self.identifier,
                    display_name=self.display_name,
                    description=self.description,
                    data_type=data_type,
                )
            ]
        )

    @property
    def fully_qualified_identifier(self) -> identifiers.FullyQualifiedPropertyIdentifier:
        if self.feature is None:
            raise UnboundLocalError()

        feature_identifier = self.feature.fully_qualified_identifier
        return identifiers.FullyQualifiedPropertyIdentifier(
            **dataclasses.asdict(feature_identifier), property=self.identifier
        )
