# StartConnection (ConnectionInit) returns (ConnectionResp) {}
import grpc
import connection_pb2
import connection_pb2_grpc

def run_client():
    channel = grpc.insecure_channel('45.76.232.143:50059')
    stub = connection_pb2_grpc.CreateWGConnectionStub(channel)
    
    request = connection_pb2.ConnectionInit(
        email="parent@email.com",
        clientPubKey="ClientPublicKey"
    )
    response = stub.StartConnection(request)
    
    print("Server Username:", response.email)
    print("Server Public Key:", response.serverPubKey)
    print("Server Port Number:", response.portNumber)
    print("Server IP Address:", response.serverIPAddr)

if __name__ == '__main__':
    run_client()
