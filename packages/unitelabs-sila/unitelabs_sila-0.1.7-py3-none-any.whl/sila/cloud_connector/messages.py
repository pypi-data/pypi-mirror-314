import dataclasses
import typing

from sila import commands, errors, protobuf


@dataclasses.dataclass
class Metadata(protobuf.BaseMessage):
    fullyQualifiedMetadataId: typing.Annotated[str, protobuf.Field(1)] = ""
    value: typing.Annotated[bytes, protobuf.Field(2)] = b""


@dataclasses.dataclass
class CommandParameter(protobuf.BaseMessage):
    metadata: typing.Annotated[typing.List[Metadata], protobuf.Field(1)] = dataclasses.field(default_factory=list)
    parameters: typing.Annotated[bytes, protobuf.Field(2)] = b""


@dataclasses.dataclass
class UnobservableCommandExecution(protobuf.BaseMessage):
    fullyQualifiedCommandId: typing.Annotated[str, protobuf.Field(1)] = ""
    commandParameter: typing.Annotated[CommandParameter, protobuf.Field(2)] = dataclasses.field(
        default_factory=CommandParameter
    )


@dataclasses.dataclass
class ObservableCommandInitiation(protobuf.BaseMessage):
    fullyQualifiedCommandId: typing.Annotated[str, protobuf.Field(1)] = ""
    commandParameter: typing.Annotated[CommandParameter, protobuf.Field(2)] = dataclasses.field(
        default_factory=CommandParameter
    )


@dataclasses.dataclass
class ObservableCommandExecutionInfoSubscription(protobuf.BaseMessage):
    commandExecutionUUID: typing.Annotated[commands.CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandExecutionUUID
    )


@dataclasses.dataclass
class ObservableCommandIntermediateResponseSubscription(protobuf.BaseMessage):
    commandExecutionUUID: typing.Annotated[commands.CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandExecutionUUID
    )


@dataclasses.dataclass
class ObservableCommandGetResponse(protobuf.BaseMessage):
    commandExecutionUUID: typing.Annotated[commands.CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandExecutionUUID
    )


@dataclasses.dataclass
class UnobservableCommandResponse(protobuf.BaseMessage):
    response: typing.Annotated[bytes, protobuf.Field(1)] = b""


@dataclasses.dataclass
class ObservableCommandConfirmation(protobuf.BaseMessage):
    commandConfirmation: typing.Annotated[commands.CommandConfirmation, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandConfirmation
    )


@dataclasses.dataclass
class ObservableCommandExecutionInfo(protobuf.BaseMessage):
    commandExecutionUUID: typing.Annotated[commands.CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandExecutionUUID
    )
    executionInfo: typing.Annotated[commands.CommandExecutionInfo, protobuf.Field(2)] = dataclasses.field(
        default_factory=commands.CommandExecutionInfo
    )


@dataclasses.dataclass
class ObservableCommandIntermediateResponse(protobuf.BaseMessage):
    commandExecutionUUID: typing.Annotated[commands.CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandExecutionUUID
    )
    response: typing.Annotated[bytes, protobuf.Field(2)] = b""


@dataclasses.dataclass
class ObservableCommandResponse(protobuf.BaseMessage):
    commandExecutionUUID: typing.Annotated[commands.CommandExecutionUUID, protobuf.Field(1)] = dataclasses.field(
        default_factory=commands.CommandExecutionUUID
    )
    response: typing.Annotated[bytes, protobuf.Field(2)] = b""


@dataclasses.dataclass
class GetFCPAffectedByMetadataRequest(protobuf.BaseMessage):
    fullyQualifiedMetadataId: typing.Annotated[str, protobuf.Field(1)] = ""


@dataclasses.dataclass
class GetFCPAffectedByMetadataResponse(protobuf.BaseMessage):
    affectedCalls: typing.Annotated[typing.List[str], protobuf.Field(1)] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class UnobservablePropertyRead(protobuf.BaseMessage):
    fullyQualifiedPropertyId: typing.Annotated[str, protobuf.Field(1)] = ""
    metadata: typing.Annotated[typing.List[Metadata], protobuf.Field(2)] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class ObservablePropertySubscription(protobuf.BaseMessage):
    fullyQualifiedPropertyId: typing.Annotated[str, protobuf.Field(1)] = ""
    metadata: typing.Annotated[typing.List[Metadata], protobuf.Field(2)] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class UnobservablePropertyValue(protobuf.BaseMessage):
    value: typing.Annotated[bytes, protobuf.Field(1)] = b""


@dataclasses.dataclass
class ObservablePropertyValue(protobuf.BaseMessage):
    value: typing.Annotated[bytes, protobuf.Field(1)] = b""


@dataclasses.dataclass
class CancelObservableCommandExecutionInfoSubscription(protobuf.BaseMessage):
    pass


@dataclasses.dataclass
class CancelObservableCommandIntermediateResponseSubscription(protobuf.BaseMessage):
    pass


@dataclasses.dataclass
class CancelObservablePropertySubscription(protobuf.BaseMessage):
    pass


# @dataclasses.dataclass
# class CreateBinaryUploadRequest(protobuf.BaseMessage):
#     metadata: typing.List[Metadata] = protobuf.field(1, default_factory=list)
#     createBinaryRequest: CreateBinaryRequest = protobuf.field(2, default_factory=CreateBinaryRequest)


@dataclasses.dataclass
class SiLAServerMessage(protobuf.BaseMessage):
    requestUUID: typing.Annotated[str, protobuf.Field(1)] = ""

    message: typing.ClassVar[protobuf.OneOf] = protobuf.OneOf()
    which_one = message.which_one_of_getter()

    unobservableCommandResponse: typing.Annotated[typing.Optional[UnobservableCommandResponse], protobuf.Field(2)] = (
        None
    )
    observableCommandConfirmation: typing.Annotated[
        typing.Optional[ObservableCommandConfirmation], protobuf.Field(3)
    ] = None
    observableCommandExecutionInfo: typing.Annotated[
        typing.Optional[ObservableCommandExecutionInfo], protobuf.Field(4)
    ] = None
    observableCommandIntermediateResponse: typing.Annotated[
        typing.Optional[ObservableCommandIntermediateResponse], protobuf.Field(5)
    ] = None
    observableCommandResponse: typing.Annotated[typing.Optional[ObservableCommandResponse], protobuf.Field(6)] = None
    getFCPAffectedByMetadataResponse: typing.Annotated[
        typing.Optional[GetFCPAffectedByMetadataResponse], protobuf.Field(7)
    ] = None
    unobservablePropertyValue: typing.Annotated[typing.Optional[UnobservablePropertyValue], protobuf.Field(8)] = None
    observablePropertyValue: typing.Annotated[typing.Optional[ObservablePropertyValue], protobuf.Field(9)] = None
    # createBinaryResponse: typing.Annotated[
    #     typing.Optional[messages.CreateBinaryResponse], protobuf.Field(10)
    # ] = None
    # uploadChunkResponse: typing.Annotated[
    #     typing.Optional[messages.UploadChunkResponse], protobuf.Field(11)
    # ] = None
    # deleteBinaryResponse: typing.Annotated[
    #     typing.Optional[messages.DeleteBinaryResponse], protobuf.Field(12)
    # ] = None
    # getBinaryResponse: typing.Annotated[
    #     typing.Optional[messages.GetBinaryInfoResponse], protobuf.Field(13)
    # ] = None
    # getChunkResponse: typing.Annotated[typing.Optional[messages.GetChunkResponse], protobuf.Field(14)] = None
    # binaryTransferError: typing.Annotated[
    #     typing.Optional[messages.BinaryTransferError], protobuf.Field(15)
    # ] = None
    commandError: typing.Annotated[typing.Optional[errors.SiLAError], protobuf.Field(16)] = None
    propertyError: typing.Annotated[typing.Optional[errors.SiLAError], protobuf.Field(17)] = None


@dataclasses.dataclass
class SiLAClientMessage(protobuf.BaseMessage):
    requestUUID: typing.Annotated[str, protobuf.Field(1)] = ""

    message: typing.ClassVar[protobuf.OneOf] = protobuf.OneOf()
    which_one = message.which_one_of_getter()

    unobservableCommandExecution: typing.Annotated[typing.Optional[UnobservableCommandExecution], protobuf.Field(2)] = (
        None
    )
    observableCommandInitiation: typing.Annotated[typing.Optional[ObservableCommandInitiation], protobuf.Field(3)] = (
        None
    )
    observableCommandExecutionInfoSubscription: typing.Annotated[
        typing.Optional[ObservableCommandExecutionInfoSubscription], protobuf.Field(4)
    ] = None
    observableCommandIntermediateResponseSubscription: typing.Annotated[
        typing.Optional[ObservableCommandIntermediateResponseSubscription], protobuf.Field(5)
    ] = None
    observableCommandGetResponse: typing.Annotated[typing.Optional[ObservableCommandGetResponse], protobuf.Field(6)] = (
        None
    )
    metadataRequest: typing.Annotated[typing.Optional[GetFCPAffectedByMetadataRequest], protobuf.Field(7)] = None
    unobservablePropertyRead: typing.Annotated[typing.Optional[UnobservablePropertyRead], protobuf.Field(8)] = None
    observablePropertySubscription: typing.Annotated[
        typing.Optional[ObservablePropertySubscription], protobuf.Field(9)
    ] = None
    cancelObservableCommandExecutionInfoSubscription: typing.Annotated[
        typing.Optional[CancelObservableCommandExecutionInfoSubscription], protobuf.Field(10)
    ] = None
    cancelObservableCommandIntermediateResponseSubscription: typing.Annotated[
        typing.Optional[CancelObservableCommandIntermediateResponseSubscription], protobuf.Field(11)
    ] = None
    cancelObservablePropertySubscription: typing.Annotated[
        typing.Optional[CancelObservablePropertySubscription], protobuf.Field(12)
    ] = None
    # createBinaryUploadRequest: typing.Annotated[
    #     typing.Optional[messages.CreateBinaryUploadRequest], protobuf.Field(13)
    # ] = None
    # deleteUploadedBinaryRequest: typing.Annotated[
    #     typing.Optional[messages.DeleteBinaryRequest], protobuf.Field(14)
    # ] = None
    # uploadChunkRequest: typing.Annotated[
    #     typing.Optional[messages.UploadChunkRequest], protobuf.Field(15)
    # ] = None
    # getBinaryInfoRequest: typing.Annotated[
    #     typing.Optional[messages.GetBinaryInfoRequest], protobuf.Field(16)
    # ] = None
    # getChunkRequest: typing.Annotated[
    #     typing.Optional[messages.GetChunkRequest], protobuf.Field(17)
    # ] = None
    # deleteDownloadedBinaryRequest: typing.Annotated[
    #     typing.Optional[messages.DeleteBinaryRequest], protobuf.Field(18)
    # ] = None
