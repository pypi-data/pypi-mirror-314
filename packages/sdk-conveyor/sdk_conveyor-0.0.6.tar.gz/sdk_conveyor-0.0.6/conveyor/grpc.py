import grpc
from grpc import Channel, RpcError, StatusCode

from conveyor.auth import get_grpc_credentials, get_grpc_target
from conveyor.auth.auth import validate_cli_version


def connect() -> Channel:
    validate_cli_version()

    return grpc.secure_channel(
        target=get_grpc_target(),
        credentials=get_grpc_credentials(),
        compression=grpc.Compression.Gzip,
    )


__all__ = ["connect", "Channel", "RpcError", "StatusCode"]
