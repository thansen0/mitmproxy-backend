# StartConnection (ConnectionInit) returns (ConnectionResp) {}
import grpc
import connection_pb2
import connection_pb2_grpc

import socket

class CreateWGConnection():

    def __init__(self, username):
        print("initialize")
        # self.server_ip_addr = socket.gethostbyname("vpn.parentcontrols.win")
        self.server_ip_addr = "45.76.232.143"
        self.server_port_num = 50051
        self.username = username

        self.clientPubKey = "pubkey"
        self.clientPrivKey = "privkey"


    def attemptConnection(self):
        channel = grpc.insecure_channel( self.server_ip_addr + ':' + str(self.server_port_num) )
        stub = connection_pb2_grpc.CreateConnectionStub(channel)

        request = connection_pb2.ConnectionInit(
            username="parent",
            clientPubKey="ClientPublicKey"
        )
        response = stub.StartConnection(request)
    
        print("Server Username:", response.username)
        print("Server Public Key:", response.serverPubKey)
        print("Server Port Number:", response.portNumber)
        print("Server IP Address:", response.serverIPAddr)


