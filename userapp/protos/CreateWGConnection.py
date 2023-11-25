# StartConnection (ConnectionInit) returns (ConnectionResp) {}
import grpc
import connection_pb2
import connection_pb2_grpc
import mitmproxy_wireguard

import socket

class CreateWGConnection():

    def __init__(self, email):
        # self.server_ip_addr = socket.gethostbyname("vpn.parentcontrols.win")
        self.server_ip_addr = "45.76.232.143"
        self.server_port_num = 50059
        self.email = email
        self.deviceId = 4 # needs to be set later

        self.client_privkey = mitmproxy_wireguard.genkey()
        self.client_pubkey  = mitmproxy_wireguard.pubkey(self.client_privkey)


    def attemptConnection(self):
        channel = grpc.insecure_channel( self.server_ip_addr + ':' + str(self.server_port_num) )
        stub = connection_pb2_grpc.CreateWGConnectionStub(channel)

        request = connection_pb2.ConnectionInit(
            email=self.email,
            clientPubKey=self.client_pubkey
        )
        response = stub.StartConnection(request)
    
        # print("Server Username:", response.email)
        print("Server Public Key:", response.serverPubKey)
        print("Server Port Number:", response.portNumber)
        print("Server IP Address:", response.serverIPAddr)
        print("certificateFileCrt:", response.certificateFileCrt)


wg = CreateWGConnection("email@email.com")
wg.attemptConnection()
