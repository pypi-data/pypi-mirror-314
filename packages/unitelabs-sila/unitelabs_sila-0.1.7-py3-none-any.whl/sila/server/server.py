from __future__ import annotations

import asyncio
import logging
import typing
import uuid

import grpc.aio
import typing_extensions

from sila import commands, core, discovery, identifiers

if typing.TYPE_CHECKING:
    from .feature import Feature


class ServerConfig(typing_extensions.TypedDict, total=False):
    host: str
    """Bind the gRPC server to this host."""

    port: typing.Union[str, int]
    """Bind the gRPC server to this port. If set to `0` an available port is chosen at runtime."""

    tls: bool
    """
    Whether to enable TLS based encryption. If enabled, a `cert` and `key` pair need to be provided.
    Defaults to `False`.
    """

    cert: bytes
    """PEM-encoded certificate chain."""

    key: bytes
    """PEM-encoded private key."""

    uuid: str
    """
    Uniquely identifies the SiLA server. Needs to remain the same even after restarting the server.
    Follows the textual representation of UUIDs, e.g. "082bc5dc-18ae-4e17-b028-6115bbc6d21e".
    """

    name: str
    """
    Human readable name of the SiLA server. This value is configurable during runtime via the SiLA
    Service feature's `set_server_name` command. Must not exceed 255 characters.
    """

    type: str
    """
    Human readable identifier of the SiLA server used to describe the entity the server represents.
    Starts with a capital letter, continued by letters and digits up to a maximum of 255 characters.
    """

    description: str
    """Describes the use and purpose of the SiLA Server."""

    version: str
    """
    The version of the SiLA server following the Semantic Versioning specification with pre-release
    identifiers separated by underscores, e.g. "3.19.373_mighty_lab_devices".
    """

    vendor_url: str
    """
    URL to the website of the vendor or the website of the product of this SiLA Server. Follows the
    Uniform Resource Locator specification in RFC 1738.
    """


class Server(core.Server):
    """
    SiLA 2 compliant gRPC server.

    A SiLA Server can either be a physical laboratory instrument or a software system that offers
    functionalities to clients. These functions are specified and described in Features.
    """

    def __init__(self, config: ServerConfig | None = None):
        config = config or {}
        super().__init__(
            uuid=config.get("uuid", str(uuid.uuid4())),
            type=config.get("type", "ExampleServer"),
            name=config.get("name", "SiLA Server"),
            version=config.get("version", "0.1"),
            description=config.get("description", ""),
            vendor_url=config.get("vendor_url", "https://github.com/UniteLabs/driver"),
        )
        self.host = config.get("host", "0.0.0.0")
        self.port = config.get("port", 0)

        if config.get("tls", False):
            cert = config.get("cert", None)
            key = config.get("key", None)

            if cert is None or key is None:
                raise ValueError("When enabling TLS based server encryption, please provide both a cert and key file.")

            self.certificate = (key, cert)
        else:
            self.certificate = None

        self.server = grpc.aio.server()
        self.running = False
        self.features: dict[identifiers.FullyQualifiedFeatureIdentifier, Feature] = {}

        self.command_executions: dict[str, commands.CommandExecution] = {}

    async def start(self):
        """Starts this Server."""
        if self.running:
            raise RuntimeError("Server is already running.")

        try:
            address = f"{self.host}:{self.port}"
            if self.certificate:
                credentials = grpc.ssl_server_credentials([self.certificate])
                self.port = self.server.add_secure_port(address, credentials)
            else:
                self.port = self.server.add_insecure_port(address)

            await self.server.start()
            self.logger.info(
                "Starting SiLA server on address '%s:%s'...", discovery.find_ip_address(self.host), self.port
            )
            self.running = True
            await self.server.wait_for_termination()
        except asyncio.CancelledError:
            await self.stop()

    async def stop(self, grace: float | None = None):
        """
        Stops this server.

        Parameters:
            grace: A grace period allowing the RPC handlers to gracefully shutdown.
        """
        self.logger.info("Stopping SiLA server...")
        await self.server.stop(grace=grace)
        self.running = False

    def add_feature(self, feature: Feature):
        """
        Registers a SiLA Feature as RPC handler with this server.

        Parameters:
            feature: The SiLA feature to add to this server.
        """
        if self.running:
            raise RuntimeError("Cannot add feature. Server is already running.")

        feature.add_to_server(self)

    def get_feature(self, identifier: str) -> Feature:
        """
        Get a registered feature.

        Parameters:
            identifier: The fully qualified feature identifier.
        """
        key = identifiers.FullyQualifiedFeatureIdentifier.parse(identifier)
        if key not in self.features:
            raise KeyError(f"Unknown feature with identifier {key}")

        return self.features[key]

    def add_command_execution(self, command_execution: commands.CommandExecution) -> None:
        if command_execution.command_execution_uuid in self.command_executions:
            raise ValueError(
                f"Command execution with uuid '{command_execution.command_execution_uuid}' already exists."
            )

        self.command_executions[command_execution.command_execution_uuid] = command_execution

    def get_command_execution(self, command_execution_uuid: str) -> commands.CommandExecution:
        if command_execution_uuid not in self.command_executions:
            raise ValueError(f"Command execution not found for uuid '{command_execution_uuid}'.")

        return self.command_executions[command_execution_uuid]

    @property
    def logger(self) -> logging.Logger:
        """A standard python :class:`~logging.Logger` for the app."""
        return logging.getLogger(__package__)
