import sys
import grpc
import socket

sys.path.append("/protos")
import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc

class ClassifyImage():

    def __init__(self, email):
        # self.server_ip_addr = socket.gethostbyname("vpn.parentcontrols.win")
        self.server_ip_addr = "127.0.0.1" # "45.76.232.143"
        self.server_port_num = 50059
        self.email = email
        self.deviceId = 4 # needs to be set later

        # read in image called headshot.jpg
        image_path = 'headshot.jpg'

        # Read the image as bytes
        with open(image_path, 'rb') as image_file:
            self.image_bytes = image_file.read()

    def attemptConnection(self):
        channel = grpc.insecure_channel( self.server_ip_addr + ':' + str(self.server_port_num) )
        stub = ic_pb2_grpc.ClassifyImageStub(channel)

        self.image = ic_pb2.NLImage(
            data=self.image_bytes,
            img_format="jpg"
        )

        request = ic_pb2.ImageMessage(
            image=self.image
        )
        print("request build", request.image.img_format)
        response = stub.StartClassification(request)
    
        # print("Server Username:", response.email)
        print("porn likelihood: ",response.porn)


wg = ClassifyImage("email@email.com")
wg.attemptConnection()
