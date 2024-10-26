import os
import grpc
import sys
import time
import signal
from dotenv import load_dotenv
from concurrent import futures
from groq import Groq
import logging
from nsfw_detector import predict
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline 

from GroqTextClassifier import ClassifyTextServicer
from ImageNetImageClassifier import ClassifyImageServicer

sys.path.append("/protos")
#import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc
#import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

def signal_handler(sig, frame):
    print("Ctrl-C pressed. Cleaning up and exiting.")
    # Perform any necessary cleanup here
    sys.exit(0)

# NOTE: uses GIL
def run_server():
    load_dotenv()
    groq_api_key = os.environ.get("GROQ_API_KEY")
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")

    groq_port_num = "50061"
    groq_server = grpc.server(futures.ThreadPoolExecutor(max_workers=16))
    tc_pb2_grpc.add_ClassifyTextServicer_to_server(ClassifyTextServicer(groq_api_key), groq_server)
    groq_server.add_insecure_port("[::]:" + groq_port_num)
    print("starting server on port " + groq_port_num)
    groq_server.start()

    img_port_num = "50060"
    img_server = grpc.server(futures.ThreadPoolExecutor(max_workers=16))
    ic_pb2_grpc.add_ClassifyImageServicer_to_server(ClassifyImageServicer(), img_server)
    img_server.add_insecure_port("[::]:" + img_port_num)
    print("starting server on port " + img_port_num)
    img_server.start()

    groq_server.wait_for_termination()
    img_server.wait_for_termination()

if __name__ == '__main__':
    # set up ctrl-c kill 
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        try:
            run_server()
        except Exception as e:
            logging.error("Server failed; restarting. Error: "+ str(e))
