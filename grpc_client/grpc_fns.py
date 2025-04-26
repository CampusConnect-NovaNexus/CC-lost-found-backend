import grpc
from . import a_pb2 as pb2
from . import a_pb2_grpc as pb2_grpc

def validate_token(token: str):
    channel = grpc.insecure_channel('localhost:50051')
    stub = pb2_grpc.AuthServiceStub(channel)
    
    token_request = pb2.Token(token=token)
    response = stub.ValidateToken(token_request)
    
    return response.is_valid
