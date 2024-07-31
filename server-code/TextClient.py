import sys
import grpc
import socket
import time

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

class ClassifyImage():
    def __init__(self):
        # self.server_ip_addr = socket.gethostbyname("vpn.parentcontrols.win")
        self.server_ip_addr = "127.0.0.1"
        self.server_port_num = 50061
        self.deviceId = 4 # needs to be set later

        # read in image called headshot.jpg
        self.tweet_text = "As a veteran of the 2000 Florida recount, I believe strongly in election integrity & the rule of law. Ignore rumors and the media narrative. This election is over when legal proceedings & recounts are completed, every legally cast vote is counted & the results are certified."

        self.prompt_text = "Please answer the following question with either a yes or no. Does the following tweet explicitly talk about US elections? \"" + self.tweet_text + "\" Please consider your answer carefully, and only reply with a yes or a no."


    def attemptConnection(self):

        try:
            channel = grpc.insecure_channel(f"{self.server_ip_addr}:{str(self.server_port_num)}" )
            stub = tc_pb2_grpc.ClassifyTextStub(channel)

            request = tc_pb2.PromptMessage(
                prompt=self.prompt_text
            )
            print("REQUEST build prompt: ", request.prompt)

            start_time = time.time()
            response = stub.StartTextClassification(request)
            end_time = time.time()
            seconds_elapsed = end_time - start_time
            print("seconds: "+str(seconds_elapsed))

            print(response.doesViolate)

        except grpc.RpcError as e:
            print(str(e))
            print("gRPC error:", e.details())
            status_code = e.code()
            print("gRPC status code:", status_code.name)
            print("gRPC status code value:", status_code.value)

        except Exception as e:
            print("An error occurred:", str(e))

wg = ClassifyImage()
wg.attemptConnection()
