import grpc
from concurrent import futures
import mitmproxy_rs
import sys
import os
import docker
import configparser
import socket
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding

sys.path.append("./protos")
import connection_pb2
import connection_pb2_grpc
import requests
import re

class CreateWGConnectionServicer(connection_pb2_grpc.CreateWGConnectionServicer):
    ip_addr = "45.76.232.143" # ip addr of server; i.e. computer this is running on

    def StartConnection(self, request, context):
        print("request: ", request)
        print("context: ", context)

        # get data from client and generate server keys
        email = str(request.email)
        deviceId = str(request.deviceId) # I only use it as a str right now, no sense converting it
        client_pubkey = request.clientPubKey
        print("request dev id: ",request.deviceId)
        print("deviceId: ", deviceId)

        # TODO uncomnment, should generate new keys each time
        server_privkey = mitmproxy_rs.genkey()
        server_pubkey  = mitmproxy_rs.pubkey(server_privkey)
        #server_privkey = 
        #server_pubkey  = mitmproxy_wireguard.pubkey(server_privkey)

        # read public .crt key
        with open('cert.crt', 'rb') as f:
            cert_content = f.read()
        cert = x509.load_pem_x509_certificate(cert_content, default_backend())
        #crt_str = cert.public_bytes(encoding=Encoding.PEM).decode()
        crt_str = cert.public_bytes(encoding=Encoding.PEM) # bytes

        # will return filters for user/device or NaN
        content_filters = self.getContentFilters(deviceId);

        # need to generate port that's not being used
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', 0))
        addr = s.getsockname()
        wireguard_port = s.getsockname()[1]
        s.close()
        print("wireguard connection port: ", wireguard_port)
        
        # create a config file for the new docker container
        docker_config = configparser.ConfigParser()
        docker_config['SERVER'] = {
            'priv_key': str(server_privkey),
            'pub_key': str(server_pubkey),
            'ip_addr': self.ip_addr,
            'wg_port': str(wireguard_port)
        }
        docker_config['CLIENT'] = {
            'pub_key': str(client_pubkey),
            'email': email,
            'content_filters': content_filters
        }
        print("email:", email)
        print("cpk:", client_pubkey)

        # TODO folder name may not be unique anymore, device will
        # but should still change
        match = re.match(r'^([^@]+)@', email)
        if match:
            email = match.group(1)
        print("new email:", email)

        #with open(email+"-docker.ini") as configfile:
        # TODO a user email will maybe eventually break this
        config_path = "user_configs/"+email+"/"+str(deviceId)+"/config.ini"
        config_path = os.path.join(os.path.abspath(os.getcwd()), config_path)
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as configfile:
            docker_config.write(configfile)

        # start docker instance independent of python
        client = docker.from_env()

        print("config_path", config_path)
        # pass the key information into docker via a volume
        volume = {
            config_path: {
                'bind': '/config.ini',
                'mode': 'ro'  # 'ro' for read-only, 'rw' for read-write
            }
        }

        # Define container settings
        container_name = email + "_" + deviceId + "_container"
        container_settings = {
            'image': 'mitmproxy:latest',  # Replace with your desired image name and tag
            'detach': True,  # Run the container in the background
            'network_mode': 'host',
            'name': container_name,  # Assign a name to the container
            'volumes': volume,
#            'remove': True, # automatically removes container when it stops
#            'ports': {
#                str(wireguard_port): 51820
#            }
        }

        # check if the container already exists, if so remove it
        try:
            existing_container = client.containers.get(container_name)
            if existing_container:
                existing_container.stop()
                existing_container.remove()
                print("DELETED existing container ", container_name)
        except:
            print("Container didn't exist")

        # TODO TODO undo comment out
        # Start the Docker container
        container = client.containers.run(**container_settings)

        # Optional: Print container ID
        print(f"Container ID: {container.id}")

        # Your server logic here
        response = connection_pb2.ConnectionResp(
            email=email,
            serverPubKey=server_pubkey,
            portNumber=wireguard_port,
            serverIPAddr=self.ip_addr,
            certificateFileCrt=crt_str
        )
        print("returning response")
        return response


    def getContentFilters(self, deviceId):
        api_url = f'http://localhost:3000/api/v1/devices/{deviceId}'  # Replace with your actual API endpoint
        try:
            response = requests.get(api_url)
        except:
            response = None
            print(f"Cannot connect to server, using defualt content filter")
            return "NaN"

        if response.status_code >= 200 and response.status_code < 300:
            return response.json()['content_filters']
        else:
            print(f"Error getting content filter, using default: {response.status_code}")
            return "NaN"

def run_server():
    port_num = "50059"
    """
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_CreateWGConnectionServicer_to_server(CreateWGConnectionServicer(), server)
    server.add_insecure_port("[::]:" + port_num)
    """
    # Load SSL certificates
    with open('protos/cert.pem', 'rb') as f:
        server_certificate = f.read()
    with open('protos/cert.key', 'rb') as f:
        server_private_key = f.read()

    server_credentials = grpc.ssl_server_credentials([(server_private_key, server_certificate)])
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_CreateWGConnectionServicer_to_server(CreateWGConnectionServicer(), server)
    server.add_secure_port("[::]:"+port_num, server_credentials)
    print("Starting listening server on port " + port_num)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
