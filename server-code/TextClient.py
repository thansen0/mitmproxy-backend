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
        self.tweet_text = "They think they erased it. People don't seem to understand that a lot of this has been captured by the Good guys. Everything they have done in every state has been recorded and proof obtained. This is a nasty war but it is a war we are going to win. All of this is going to be released to the public.  Watch for it.  We are almost there."
        self.tweet_text = "What an absolute pussy. If my kids die at the hands of some disgusting mud/cat/human-eating, low-IQ Haitian, I want a pitchfork mob to cut their ancestral tree to a stump. wtf is wrong with people"
        self.tweet_text = "trans rights are human rights."

        self.prompt_text = "You are a fast AI bot tasked with quickly classifying text content on whether it supports a certain ideology. Please answer the following question with either a YES or NO. Does the following tweet explicitly discuss [trans, lgbt, atheism, socialism, communism] favorably? \"" + self.tweet_text + "\" Remember: only reply with a YES or a NO on whether they support a mentioned topic."


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
