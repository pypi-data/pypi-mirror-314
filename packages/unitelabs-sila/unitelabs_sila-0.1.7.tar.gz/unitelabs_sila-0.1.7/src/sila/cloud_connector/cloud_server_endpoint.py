from __future__ import annotations

import asyncio
import io
import logging
import typing
import weakref

import grpc
import grpc.aio
import grpc.experimental
import typing_extensions

from sila import commands, errors
from sila.server import (
    ObservableCommand,
    ObservableProperty,
    Server,
    UnobservableCommand,
    UnobservableProperty,
)

from . import messages


class CloudServerEndpointConfig(typing_extensions.TypedDict, total=False):
    endpoint: str
    secure: bool
    options: dict


class Context:
    _callback: typing.Optional[typing.Callable] = None
    running = False

    def add_callback(self, callback: typing.Callable):
        self._callback = callback
        self.running = True

    def cancel(self):
        self.running = False
        if self._callback:
            self._callback()


class Responses(asyncio.Queue):
    def __init__(self, logger):
        super().__init__()
        self.logger = logger

    def __aiter__(self):
        return self

    async def __anext__(self):
        message = await self.get()
        return message


class CloudServerEndpoint:
    """gRPC client for SiLA cloud connectivity"""

    def __init__(self, server: Server, config: CloudServerEndpointConfig | None = None):
        self.__config = config or {}
        self._channel: typing.Optional[grpc.aio.Channel] = None
        self.responses = Responses(self.logger)
        self.server: Server = weakref.proxy(server)
        self.subscriptions: dict[str, asyncio.Task] = {}

    async def start(self):
        """Starts this client."""
        address = self.__config.get("endpoint", "localhost:5000")
        self.logger.info("Starting cloud server endpoint on address '%s'...", address)

        options: grpc.aio.ChannelArgumentType = list(self.__config.get("options", {}).items())

        try:
            if self.__config.get("secure"):
                credentials = grpc.ssl_channel_credentials(None)
                self._channel = grpc.aio.secure_channel(address, credentials=credentials, options=options)
            else:
                self._channel = grpc.aio.insecure_channel(address, options=options)

            await self._channel.channel_ready()
            self.logger.info("Connection established.")
            self.responses = Responses(self.logger)

            listen = self._channel.stream_stream(
                method="/sila2.org.silastandard.CloudClientEndpoint/ConnectSiLAServer",
                request_serializer=bytes,
                response_deserializer=lambda x: messages.SiLAClientMessage.read_from(io.BytesIO(x)),
            )
            response_iterator = listen(request_iterator=self.responses.__aiter__(), wait_for_ready=True)

            async for response in response_iterator.__aiter__():
                await self.receive(response)

        except asyncio.CancelledError:
            await self.stop()
            return
        except grpc.aio.AioRpcError as error:
            self.logger.error("Connection dropped. %s", error)
        except Exception as error:  # pylint: disable=broad-exception-caught
            self.logger.error(error)

        await self.stop()
        await asyncio.sleep(10)
        await self.start()

    async def stop(self, grace: typing.Optional[float] = None):
        """Stops this client."""
        self.logger.info("Stopping cloud server endpoint...")
        for subscription in self.subscriptions.values():
            subscription.cancel()
        if self._channel:
            await self._channel.close(grace=grace)

    @property
    def logger(self) -> logging.Logger:
        """A standard Python :class:`~logging.Logger` for the app."""
        return logging.getLogger(__package__)

    async def receive(self, client_message: messages.SiLAClientMessage):
        if client_message.unobservableCommandExecution is not None:
            asyncio.create_task(
                self.unobservable_command_execution(
                    client_message.requestUUID,
                    client_message.unobservableCommandExecution.fullyQualifiedCommandId,
                    client_message.unobservableCommandExecution.commandParameter.parameters,
                    self.parse_metadata(client_message.unobservableCommandExecution.commandParameter.metadata),
                )
            )

        if client_message.observableCommandInitiation is not None:
            asyncio.create_task(
                self.observable_command_initiation(
                    client_message.requestUUID,
                    client_message.observableCommandInitiation.fullyQualifiedCommandId,
                    client_message.observableCommandInitiation.commandParameter.parameters,
                    self.parse_metadata(client_message.observableCommandInitiation.commandParameter.metadata),
                )
            )

        if client_message.observableCommandExecutionInfoSubscription is not None:
            asyncio.create_task(
                self.observable_command_execution_info_subscription(
                    client_message.requestUUID,
                    client_message.observableCommandExecutionInfoSubscription.commandExecutionUUID,
                )
            )

        if client_message.cancelObservableCommandExecutionInfoSubscription is not None:
            asyncio.create_task(
                self.cancel_observable_command_execution_info_subscription(
                    client_message.requestUUID,
                )
            )

        if client_message.observableCommandIntermediateResponseSubscription is not None:
            asyncio.create_task(
                self.observable_command_intermediate_response_subscription(
                    client_message.requestUUID,
                    client_message.observableCommandIntermediateResponseSubscription.commandExecutionUUID,
                )
            )

        if client_message.cancelObservableCommandIntermediateResponseSubscription is not None:
            asyncio.create_task(
                self.cancel_observable_command_intermediate_response_subscription(
                    client_message.requestUUID,
                )
            )

        if client_message.observableCommandGetResponse is not None:
            asyncio.create_task(
                self.observable_command_get_response(
                    client_message.requestUUID,
                    client_message.observableCommandGetResponse.commandExecutionUUID,
                )
            )

        if client_message.unobservablePropertyRead is not None:
            asyncio.create_task(
                self.unobservable_property_read(
                    client_message.requestUUID,
                    client_message.unobservablePropertyRead.fullyQualifiedPropertyId,
                    self.parse_metadata(client_message.unobservablePropertyRead.metadata),
                )
            )

        if client_message.observablePropertySubscription is not None:
            asyncio.create_task(
                self.observable_property_subscription(
                    client_message.requestUUID,
                    client_message.observablePropertySubscription.fullyQualifiedPropertyId,
                    self.parse_metadata(client_message.observablePropertySubscription.metadata),
                )
            )

        if client_message.cancelObservablePropertySubscription is not None:
            asyncio.create_task(self.cancelObservablePropertySubscription(client_message.requestUUID))

    async def unobservable_command_execution(
        self, request_uuid: str, identifier: str, parameters: bytes, metadata: dict
    ):
        try:
            feature = self.server.get_feature(identifier=identifier)
            unobservable_command = feature.get_command(identifier=identifier)

            if not isinstance(unobservable_command, UnobservableCommand):
                raise ValueError()

            responses = await unobservable_command.execute(parameters, metadata)
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                unobservableCommandResponse=messages.UnobservableCommandResponse(response=responses),
            )
            await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                commandError=errors.SiLAError.from_exception(error),
            )
            await self.responses.put(message)

    async def observable_command_initiation(
        self, request_uuid: str, identifier: str, parameters: bytes, metadata: dict
    ):
        try:
            feature = self.server.get_feature(identifier=identifier)
            observable_command = feature.get_command(identifier=identifier)

            if not isinstance(observable_command, ObservableCommand):
                raise ValueError()

            command_confirmation = await observable_command.initiate_command(parameters, metadata)
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                observableCommandConfirmation=messages.ObservableCommandConfirmation(
                    commandConfirmation=command_confirmation
                ),
            )
            await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid, commandError=errors.SiLAError.from_exception(error)
            )
            await self.responses.put(message)

    async def observable_command_execution_info_subscription(
        self, request_uuid: str, command_execution_uuid: commands.CommandExecutionUUID
    ):
        try:
            command_execution = self.server.get_command_execution(command_execution_uuid=command_execution_uuid.value)

            feature = self.server.get_feature(identifier=str(command_execution.identifier))
            observable_command = feature.get_command(identifier=str(command_execution.identifier))

            if not isinstance(observable_command, ObservableCommand):
                raise ValueError()

            if current_task := asyncio.current_task():
                self.subscriptions[request_uuid + "_info"] = current_task

            async for responses in observable_command.subscribe_status(command_execution.command_execution_uuid):
                message = messages.SiLAServerMessage(
                    requestUUID=request_uuid,
                    observableCommandExecutionInfo=messages.ObservableCommandExecutionInfo(
                        commandExecutionUUID=commands.CommandExecutionUUID(
                            value=command_execution.command_execution_uuid
                        ),
                        executionInfo=responses,
                    ),
                )
                await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                commandError=errors.SiLAError.from_exception(error),
            )
            await self.responses.put(message)

    async def cancel_observable_command_execution_info_subscription(self, request_uuid: str):
        if request_uuid + "_info" in self.subscriptions:
            self.subscriptions.pop(request_uuid + "_info").cancel()

    async def observable_command_intermediate_response_subscription(
        self, request_uuid: str, command_execution_uuid: commands.CommandExecutionUUID
    ):
        try:
            command_execution = self.server.get_command_execution(command_execution_uuid=command_execution_uuid.value)

            feature = self.server.get_feature(identifier=str(command_execution.identifier))
            observable_command = feature.get_command(identifier=str(command_execution.identifier))

            if not isinstance(observable_command, ObservableCommand):
                raise ValueError()

            if current_task := asyncio.current_task():
                self.subscriptions[request_uuid + "_intermediate"] = current_task

            async for responses in observable_command.subscribe_intermediate(command_execution.command_execution_uuid):
                message = messages.SiLAServerMessage(
                    requestUUID=request_uuid,
                    observableCommandIntermediateResponse=messages.ObservableCommandIntermediateResponse(
                        commandExecutionUUID=commands.CommandExecutionUUID(
                            value=command_execution.command_execution_uuid
                        ),
                        response=responses,
                    ),
                )
                await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                commandError=errors.SiLAError.from_exception(error),
            )
            await self.responses.put(message)

    async def cancel_observable_command_intermediate_response_subscription(self, request_uuid: str):
        if request_uuid + "_intermediate" in self.subscriptions:
            self.subscriptions.pop(request_uuid + "_intermediate").cancel()

    async def observable_command_get_response(
        self, request_uuid: str, command_execution_uuid: commands.CommandExecutionUUID
    ):
        try:
            command_execution = self.server.get_command_execution(command_execution_uuid=command_execution_uuid.value)

            feature = self.server.get_feature(identifier=str(command_execution.identifier))
            observable_command = feature.get_command(identifier=str(command_execution.identifier))

            if not isinstance(observable_command, ObservableCommand):
                raise ValueError()

            response = await observable_command.get_result(command_execution.command_execution_uuid)

            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                observableCommandResponse=messages.ObservableCommandResponse(
                    commandExecutionUUID=commands.CommandExecutionUUID(value=command_execution.command_execution_uuid),
                    response=response,
                ),
            )
            await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                commandError=errors.SiLAError.from_exception(error),
            )
            await self.responses.put(message)

    async def unobservable_property_read(self, request_uuid: str, identifier: str, metadata: dict):
        try:
            feature = self.server.get_feature(identifier=identifier)
            unobservable_property = feature.get_property(identifier=identifier)

            if not isinstance(unobservable_property, UnobservableProperty):
                raise ValueError()

            responses = await unobservable_property.execute(metadata)
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid, unobservablePropertyValue=messages.UnobservablePropertyValue(value=responses)
            )
            await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                propertyError=errors.SiLAError.from_exception(error),
            )
            await self.responses.put(message)

    async def observable_property_subscription(self, request_uuid: str, identifier: str, metadata: dict):
        try:
            feature = self.server.get_feature(identifier=identifier)
            observable_property = feature.get_property(identifier=identifier)

            if not isinstance(observable_property, ObservableProperty):
                raise ValueError()

            if current_task := asyncio.current_task():
                self.subscriptions[request_uuid] = current_task

            async for responses in observable_property.execute(metadata):
                message = messages.SiLAServerMessage(
                    requestUUID=request_uuid,
                    observablePropertyValue=messages.ObservablePropertyValue(value=responses),
                )
                await self.responses.put(message)
        except errors.SiLAException as error:
            message = messages.SiLAServerMessage(
                requestUUID=request_uuid,
                propertyError=errors.SiLAError.from_exception(error),
            )
            await self.responses.put(message)

    async def cancelObservablePropertySubscription(self, request_uuid: str):
        if request_uuid in self.subscriptions:
            self.subscriptions.pop(request_uuid).cancel()

    def parse_metadata(self, metadata: list[messages.Metadata]) -> dict[str, typing.Any]:
        return {
            f"sila-{metadatum.fullyQualifiedMetadataId.replace('/', '-').lower()}-bin": metadatum.value
            for metadatum in metadata
        }
