from __future__ import annotations

import abc
import dataclasses
import typing
import weakref

import grpc
import grpc.aio

from sila import data_types, identifiers, metadata

if typing.TYPE_CHECKING:
    from sila import core

    from .feature import Feature


@dataclasses.dataclass
class Metadata(metadata.Metadata):
    @abc.abstractmethod
    def affects(self) -> list[identifiers.FullyQualifiedIdentifier]: ...

    @abc.abstractmethod
    def intercept(self, handler: core.Handler, metadata_: dict): ...

    def execute(
        self,
        message,  # pylint: disable=unused-argument
        context: grpc.aio.ServicerContext,  # pylint: disable=unused-argument
    ) -> bytes:
        return bytes(
            metadata.Metadata.AffectedByResponse(
                [data_types.String.Message(value=str(affects)) for affects in self.affects()]
            )
        )

    def add_to_feature(self, feature: Feature):
        """
        Registers this metadata as RPC handler with a SiLA feature.

        Args:
            feature: The SiLA feature to add this metadata to.
        """
        self.feature = weakref.proxy(feature)
        feature.metadata[self.fully_qualified_identifier] = self
        feature.handlers[f"Get_FCPAffectedByMetadata_{self.identifier}"] = grpc.unary_unary_rpc_method_handler(
            self.execute
        )
