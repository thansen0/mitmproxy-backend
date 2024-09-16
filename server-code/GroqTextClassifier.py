import os
import grpc
import sys
import time
import signal
from dotenv import load_dotenv
from concurrent import futures
from groq import Groq
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 
# pip install accelerate

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class ClassifyTextServicer(tc_pb2_grpc.ClassifyTextServicer):
    def __init__(self, groq_api_key):
        self.debug = True

        print("GROQ api key: "+ str(groq_api_key))
        self.client = Groq(
            api_key=groq_api_key,
        )


    def StartTextClassification(self, request, context):
        print(f"Input text: {request.prompt}")

        start_time = time.time()
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{request.prompt}",
                }
            ],
            #model="llama3-8b-8192", # 0.65 s
            model="mixtral-8x7b-32768", # 0.35 s
        )
        end_time = time.time()
        output = chat_completion.choices[0].message.content

        print(output)
        if self.debug:
            logging.info("Prompt output: " + chat_completion.choices[0].message.content)

        does_violate = "yes" in output.lower()
        response = tc_pb2.PromptResponse(doesViolate=does_violate)
        seconds_elapsed = end_time - start_time
        print("seconds: "+str(seconds_elapsed))

        return response

def signal_handler(sig, frame):
    print("Ctrl-C pressed. Cleaning up and exiting.")
    # Perform any necessary cleanup here
    sys.exit(0)

# NOTE: uses GIL
def run_server():
    port_num = "50061"
    load_dotenv()
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=16))
    tc_pb2_grpc.add_ClassifyTextServicer_to_server(ClassifyTextServicer(groq_api_key), server)
    server.add_insecure_port("[::]:" + port_num)
    print("starting server on port " + port_num)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    # set up ctrl-c kill 
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            run_server()
        except Exception as e:
            logging.error("Server failed; restarting. Error: "+ str(e))
