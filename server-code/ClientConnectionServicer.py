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
    ip_addr = "45.76.232.143" # ip addr of server; i.e. computer this is running on

    def StartConnection(self, request, context):
        print("request: ", request)
        print("context: ", context)

        # get data from client and generate server keys
        email = str(request.email)
        deviceId = str(request.deviceId) # I only use it as a str right now, no sense converting it
        client_pubkey = request.clientPubKey

        server_privkey = mitmproxy_wireguard.genkey()
        server_pubkey  = mitmproxy_wireguard.pubkey(server_privkey)

        # will return filters for user/device or NaN
        content_filters = getContentFilters(deviceId);

        # create a config file for the new docker container
        docker_config = configparser.ConfigParser()
        docker_config['SERVER'] = {
            'priv_key': str(server_privkey),
            'pub_key': str(server_pubkey),
            'ip_addr': self.ip_addr
        }
        docker_config['CLIENT'] = {
            'pub_key': str(client_pubkey),
            'email': email,
            'content_filters': content_filters
        }
        print("email:", email)
        print("cpk:", client_pubkey)
        #with open(email+"-docker.ini") as configfile:
        # TODO a user email will maybe eventually break this
        config_path = "./user_configs/"+email+"/"+str(deviceId)+"/config.ini"
        config_path = os.path.join(os.path.abspath(os.getcwd()), config_path)
        os.makedirs(os.path.dirname(config_path), exist_ok=True)
        with open(config_path, "w") as configfile:
            docker_config.write(configfile)

        # start docker instance independent of python
        client = docker.from_env()

        print("config_path",config_path)
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
            'name': container_name,  # Assign a name to the container
            'volumes': volume,
#            'remove': True, # automatically removes container when it stops
            'ports': {
                '51820': 51820
            }
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

        # Start the Docker container
        container = client.containers.run(**container_settings)

        # Optional: Print container ID
        print(f"Container ID: {container.id}")

        # Your server logic here
        response = connection_pb2.ConnectionResp(
            email=email,
            serverPubKey=server_pubkey,
            portNumber=5000,
            serverIPAddr=self.ip_addr
        )
        print("returning response")
        return response


    def getContentFilters(deviceId):
        api_url = f'http://localhost:3000/api/v1/devices/{deviceId}'  # Replace with your actual API endpoint
        response = requests.get(api_url)

        if response.status_code >= 200 and response.status_code < 300:
            return response.json()['content_filters']
        else:
            print(f"Error getting content filter, using default: {response.status_code}")
            return "NaN"

def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    connection_pb2_grpc.add_CreateConnectionServicer_to_server(CreateConnectionServicer(), server)
    server.add_insecure_port("[::]:50051")

    print("Starting listening server")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
