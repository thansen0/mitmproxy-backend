import grpc
from concurrent import futures
import sys

sys.path.append("/protos")
import protos.connection_pb2 as connection_pb2
import protos.connection_pb2_grpc as connection_pb2_grpc
#import connection_pb2
#import connection_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class CreateConnectionServicer(connection_pb2_grpc.CreateConnectionServicer):
    def StartConnection(self, request, context):
        # Your server logic here
        response = connection_pb2.ConnectionResp(
            email="parent@email.com",
            serverPubKey="ServerPublicKey",
            portNumber=5000,
            serverIPAddr="45.76.232.143",
            certificateFileCrt="cert file crt"
        )
        print("returning response: ", response)
        return response

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_CreateConnectionServicer_to_server(CreateConnectionServicer(), server)
    server.add_insecure_port("[::]:50051")
    print("starting server")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
