import grpc
import os
from . import a_pb2 as pb2
from . import a_pb2_grpc as pb2_grpc
from ..config import Config

def validate_token(token: str):
    grpc_server = os.getenv('AUTH_GRPC_SERVER') or os.getenv('GRPC_SERVER_ADDRESS') or Config.GRPC_SERVER
    print(f"Connecting to gRPC server at: {grpc_server}")
    
    channel = grpc.insecure_channel(grpc_server)
    stub = pb2_grpc.AuthServiceStub(channel)
    
    token_request = pb2.Token(token=token)
    response = stub.ValidateToken(token_request)
    
    return response.is_valid
