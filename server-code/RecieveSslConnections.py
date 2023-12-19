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
class CreateWGConnectionServicer(connection_pb2_grpc.CreateWGConnectionServicer):
    def StartConnection(self, request, context):
        with open("cert.crt", 'rb') as f:
            certFileCrt = f.read()
        # Your server logic here
        response = connection_pb2.ConnectionResp(
            email="parent@email.com",
            serverPubKey="ServerPublicKey",
            portNumber=5000,
            serverIPAddr="45.76.232.143",
            certificateFileCrt=certFileCrt
        )
        print("returning response: ", response)
        return response

def run_server():
    port_num = "50059"

    # Load SSL certificates
    with open('protos/cert.pem', 'rb') as f:
        server_certificate = f.read()
    with open('protos/cert.key', 'rb') as f:
        server_private_key = f.read()

    server_credentials = grpc.ssl_server_credentials([(server_private_key, server_certificate)])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_CreateWGConnectionServicer_to_server(CreateWGConnectionServicer(), server)
    server.add_secure_port("[::]:"+port_num, server_credentials)
    print("starting server on port " + port_num)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
