from __future__ import annotations

import dataclasses
import typing
import weakref

import grpc

from sila import core, identifiers

from .handler import Handler
from .metadata import Metadata

if typing.TYPE_CHECKING:
    from sila.data_types import DataTypeDefinition

    from .server import Server


@dataclasses.dataclass
class Feature(core.Feature):
    metadata: dict[identifiers.FullyQualifiedMetadataIdentifier, Metadata] = dataclasses.field(
        init=False, repr=False, default_factory=dict
    )

    handlers: dict[str, grpc.RpcMethodHandler] = dataclasses.field(init=False, repr=False, default_factory=dict)
    """A dictionary that maps method names to corresponding RpcMethodHandler."""

    server: Server | None = dataclasses.field(init=False, repr=False, default=None)
    """The SiLA server this feature was registered with."""

    def add_to_server(self, server: Server) -> None:
        """
        Registers this feature as RPC handler with a SiLA server.

        Args:
            server: The SiLA server to add this feature to.
        """
        server.features[self.fully_qualified_identifier] = self
        self.server = weakref.proxy(server)

        service = ".".join(
            (
                "sila2",
                self.originator,
                self.category,
                str(self.identifier).lower(),
                f"v{self.version.rpartition('.')[0]}",
                self.identifier,
            )
        )

        handlers = grpc.method_handlers_generic_handler(service, self.handlers)
        server.server.add_generic_rpc_handlers((handlers,))

    def add_handler(self, handler: Handler):
        handler.add_to_feature(self)

    def add_metadata(self, metadata: Metadata):
        metadata.add_to_feature(self)

    def add_data_type_definition(self, data_type_definition: DataTypeDefinition):
        data_type_definition.add_to_feature(self)
