from __future__ import annotations

import base64
import dataclasses
import functools
import inspect
import io
from collections.abc import AsyncIterator

import grpc.aio

from sila import commands, errors, protobuf

from .handler import Handler


@dataclasses.dataclass
class ObservableCommand(commands.ObservableCommand, Handler):
    async def initiate_command(self, message: bytes, metadata: dict) -> commands.CommandConfirmation:
        if self.feature is None or self.feature.server is None:
            raise RuntimeError("Cannot initiate unbound command.")

        try:
            for feature in self.feature.server.features.values():
                for interceptor in feature.metadata.values():
                    interceptor.intercept(self, metadata)
        except errors.DefinedExecutionError as error:
            raise errors.FrameworkError(
                error_type=errors.FrameworkError.Type.INVALID_METADATA, message=error.description
            )
        try:
            parameters = self.parameters.decode(message)
        except protobuf.MessageDecodeError as error:
            raise errors.ValidationError(
                parameter=f"{self.fully_qualified_identifier}/Parameter/{error.field}", message=error.msg
            )
        try:
            command_execution = commands.CommandExecution(
                identifier=self.fully_qualified_identifier,
                executable=functools.partial(self.execute, parameters=parameters),
            )
            self.feature.server.add_command_execution(command_execution)
            command_execution.run()

            return command_execution.command_confirmation
        except errors.DefinedExecutionError as error:
            error.feature = self.feature
            raise error
        except errors.SiLAException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise errors.UndefinedExecutionError(str(error))

    async def initiate_rpc_method_handler(
        self, message: bytes, context: grpc.aio.ServicerContext
    ) -> commands.CommandConfirmation | None:
        """The command initiation triggers the execution of the command."""
        try:
            metadata = dict(context.invocation_metadata() or {})
            return await self.initiate_command(message, metadata)
        except errors.SiLAException as error:
            exception = errors.SiLAError.from_exception(error)
            details = base64.standard_b64encode(bytes(exception)).decode("ascii")
            await context.abort(code=grpc.StatusCode.ABORTED, details=details)

    async def subscribe_status(
        self,
        command_execution_uuid: str,
        context: grpc.aio.ServicerContext | None = None,  # pylint: disable=unused-argument
    ) -> AsyncIterator[commands.CommandExecutionInfo]:
        if self.feature is None or self.feature.server is None:
            raise errors.FrameworkError(
                error_type=errors.FrameworkError.Type.INVALID_COMMAND_EXECUTION_UUID,
                message="Invalid Command Execution UUID.",
            )

        command_execution = self.feature.server.get_command_execution(command_execution_uuid)

        while True:
            await command_execution.execution_info.wait()
            yield command_execution.command_execution_info
            command_execution.execution_info.clear()

    async def subscribe_intermediate(
        self,
        command_execution_uuid: str,
        context: grpc.aio.ServicerContext | None = None,  # pylint: disable=unused-argument
    ) -> AsyncIterator[bytes]:
        if self.feature is None or self.feature.server is None:
            raise RuntimeError("Cannot subscribe intermediate responses of unbound command.")

        command_execution = self.feature.server.get_command_execution(command_execution_uuid)

        if self.intermediate_responses is None:
            raise RuntimeError("Command has no intermediate responses")

        while True:
            responses = await command_execution.intermediate_responses.get()

            if inspect.isawaitable(responses):
                responses = await responses

            if isinstance(responses, type(None)):
                responses = {}
            if isinstance(responses, tuple):
                responses = {
                    element.identifier: responses[index]
                    for index, element in enumerate(self.intermediate_responses.elements)
                }
            if not isinstance(responses, dict):
                responses = {self.intermediate_responses.elements[0].identifier: responses}

            yield self.intermediate_responses.encode(responses)
            command_execution.intermediate_responses.task_done()

    async def get_result(self, command_execution_uuid: str) -> bytes:
        if self.feature is None or self.feature.server is None:
            raise RuntimeError("Cannot get result of unbound command.")

        command_execution = self.feature.server.get_command_execution(command_execution_uuid)

        if command_execution.command_execution_status == commands.CommandExecutionStatus.RUNNING:
            raise errors.FrameworkError(
                error_type=errors.FrameworkError.Type.COMMAND_EXECUTION_NOT_FINISHED,
                message="Command is still in running",
            )

        if command_execution.command_execution_status == commands.CommandExecutionStatus.FINISHED_WITH_ERROR:
            raise command_execution.exception or errors.UndefinedExecutionError(message="An undefined error occured")

        if command_execution.command_execution_status == commands.CommandExecutionStatus.FINISHED_SUCCESSFULLY:
            return command_execution.responses or b""

        return b""

    async def result_rpc_method_handler(self, command_execution_uuid: str, context: grpc.aio.ServicerContext) -> bytes:
        try:
            return await self.get_result(command_execution_uuid)
        except errors.SiLAException as error:
            exception = errors.SiLAError.from_exception(error)
            details = base64.standard_b64encode(bytes(exception)).decode("ascii")
            await context.abort(code=grpc.StatusCode.ABORTED, details=details)

    async def execute(self, parameters: dict, command_execution: commands.CommandExecution):
        try:
            responses = self.function(**parameters, command_execution=command_execution)
            if inspect.isawaitable(responses):
                responses = await responses

            response = self.responses.encode(responses)
            command_execution.send_responses(response)
        except errors.DefinedExecutionError as error:
            error.feature = self.feature
            command_execution.raise_exception(error)
        except errors.SiLAException as error:
            command_execution.raise_exception(error)
        except Exception as error:  # pylint: disable=broad-exception-caught
            command_execution.raise_exception(errors.UndefinedExecutionError(str(error)))

    def add_to_feature(self, feature):
        super().add_to_feature(feature=feature)
        feature.commands[self.fully_qualified_identifier] = self

        feature.handlers[f"{self.identifier}"] = grpc.unary_unary_rpc_method_handler(
            self.initiate_rpc_method_handler, response_serializer=bytes
        )

        feature.handlers[f"{self.identifier}_Info"] = grpc.unary_stream_rpc_method_handler(
            self.subscribe_status,
            request_deserializer=lambda x: commands.CommandExecutionUUID.read_from(io.BytesIO(x)).value,
            response_serializer=bytes,
        )

        if self.intermediate_responses:
            feature.handlers[f"{self.identifier}_Intermediate"] = grpc.unary_stream_rpc_method_handler(
                self.subscribe_intermediate,
                request_deserializer=lambda x: commands.CommandExecutionUUID.read_from(io.BytesIO(x)).value,
            )

        feature.handlers[f"{self.identifier}_Result"] = grpc.unary_unary_rpc_method_handler(
            self.result_rpc_method_handler,
            request_deserializer=lambda x: commands.CommandExecutionUUID.read_from(io.BytesIO(x)).value,
        )
