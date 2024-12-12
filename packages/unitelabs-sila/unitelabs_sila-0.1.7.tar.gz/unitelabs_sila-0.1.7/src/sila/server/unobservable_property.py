from __future__ import annotations

import base64
import dataclasses
import inspect

import grpc
import grpc.aio

from sila import errors, properties

from .handler import Handler


@dataclasses.dataclass
class UnobservableProperty(properties.UnobservableProperty, Handler):
    async def execute(self, metadata: dict) -> bytes:
        if self.feature is None or self.feature.server is None:
            raise RuntimeError("Cannot execute unbound property.")

        try:
            for feature in self.feature.server.features.values():
                for interceptor in feature.metadata.values():
                    interceptor.intercept(self, metadata)
        except errors.DefinedExecutionError as error:
            raise errors.FrameworkError(
                error_type=errors.FrameworkError.Type.INVALID_METADATA, message=error.description
            )
        try:
            responses = self.function()
            if inspect.isawaitable(responses):
                responses = await responses

            return self.message.encode({self.identifier: responses})
        except errors.DefinedExecutionError as error:
            error.feature = self.feature
            raise error
        except errors.SiLAException as error:
            raise error
        except Exception as error:  # pylint: disable=broad-exception-caught
            raise errors.UndefinedExecutionError(str(error))

    async def rpc_method_handler(
        self,
        message: bytes,  # pylint: disable=unused-argument
        context: grpc.aio.ServicerContext,
    ) -> bytes:
        """
        The implementation of the RPC handler that accepts one request and returns either one response or an iterator of
        response values.

        Parameters:
            message: The binary representation of the request message.
            context: A context object of the RPC call.

        Returns:
            The binary representation of the response message.
        """
        try:
            metadata = dict(context.invocation_metadata() or {})
            return await self.execute(metadata)
        except errors.SiLAException as error:
            exception = errors.SiLAError.from_exception(error)
            details = base64.standard_b64encode(bytes(exception)).decode("ascii")
            await context.abort(code=grpc.StatusCode.ABORTED, details=details)

    def add_to_feature(self, feature):
        super().add_to_feature(feature=feature)
        feature.properties[self.fully_qualified_identifier] = self
        feature.handlers[f"Get_{self.identifier}"] = grpc.unary_unary_rpc_method_handler(self.rpc_method_handler)
