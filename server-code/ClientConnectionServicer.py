import grpc
from concurrent import futures
import mitmproxy_wireguard
import sys
import os
import docker
import configparser

sys.path.append("./protos")
import connection_pb2
import connection_pb2_grpc

class CreateConnectionServicer(connection_pb2_grpc.CreateConnectionServicer):
    ip_addr = "45.76.232.143"

    def StartConnection(self, request, context):
        print("request: ", request)
        print("context: ", context)

        # get data from client and generate server keys
        username = str(request.username)
        deviceId = str(request.deviceId) # I only use it as a str right now, no sense converting it
        client_pubkey = request.clientPubKey

        server_privkey = mitmproxy_wireguard.genkey()
        server_pubkey  = mitmproxy_wireguard.pubkey(server_privkey)

        # create a config file for the new docker container
        docker_config = configparser.ConfigParser()
        docker_config['SERVER'] = {
            'priv_key': str(server_privkey),
            'pub_key': str(server_pubkey),
            'ip_addr': self.ip_addr
        }
        docker_config['CLIENT'] = {
            'pub_key': str(client_pubkey),
            'username': username
        }
        print("username:", username)
        print("cpk:", client_pubkey)
        #with open(username+"-docker.ini") as configfile:
        # TODO a user email will eventually break this
        config_path = "./user_configs/"+username+"/"+str(deviceId)+"/config.ini"
        config_path = os.path.join(os.path.abspath(os.getcwd()), config_path)
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as configfile:
            docker_config.write(configfile)

        # start docker instance independent of python
        client = docker.from_env()

        # pass the key information into docker via a volume
        volume = {
            '/': {
                'bind': config_path,
                'mode': 'ro'  # 'ro' for read-only, 'rw' for read-write
            }
        }

        # Define container settings
        container_name = username + "_" + deviceId + "_container"
        container_settings = {
            'image': 'mitmproxy:latest',  # Replace with your desired image name and tag
            'detach': True,  # Run the container in the background
            'name': container_name,  # Assign a name to the container
            'volumes': volume,
            'remove': True # automatically removes container when it stops
        }

        # check if the container already exists, if so remove it
        try:
            existing_container = client.containers.get(container_name)
            if existing_container:
                existing_container.stop()
                existing_container.remove()
                print("DELETed existing container ", container_name)
        except:
            print("Container didn't exist")

        # Start the Docker container
        container = client.containers.run(**container_settings)

        # Optional: Print container ID
        print(f"Container ID: {container.id}")

        # Your server logic here
        response = connection_pb2.ConnectionResp(
            username=username,
            serverPubKey=server_pubkey,
            portNumber=5000,
            serverIPAddr=self.ip_addr
        )
        print("returning response")
        return response

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_CreateConnectionServicer_to_server(CreateConnectionServicer(), server)
    server.add_insecure_port("[::]:50051")

    print("Starting listening server")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
