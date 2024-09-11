import os
import grpc
import sys
import time
import signal
from concurrent import futures
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
    def __init__(self):
        self.debug = True

        torch.random.manual_seed(0) 
        self.model = AutoModelForCausalLM.from_pretrained( 
            "microsoft/Phi-3-mini-128k-instruct",  
#            attn_implementation='eager',
            device_map="cuda",  
            torch_dtype="auto",  
            trust_remote_code=True,  
        ) 

        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct") 


        self.pipe = pipeline( 
            "text-generation", 
            model=self.model, 
            tokenizer=self.tokenizer, 
        ) 

        self.generation_args = { 
            "max_new_tokens": 500, 
            "return_full_text": False, 
            "temperature": 0.0, 
            "do_sample": False, 
        } 

        if self.debug:
            messages = [ 
                {"role": "system", "content": "You are a helpful AI assistant."}, 
                {"role": "user", "content": "Can you provide ways to eat combinations of bananas and dragonfruits?"}, 
                {"role": "assistant", "content": "Sure! Here are some ways to eat bananas and dragonfruits together: 1. Banana and dragonfruit smoothie: Blend bananas and dragonfruits together with some milk and honey. 2. Banana and dragonfruit salad: Mix sliced bananas and dragonfruits together with some lemon juice and honey."}, 
                {"role": "user", "content": "What about solving an 2x + 3 = 7 equation?"}, 
            ]

            output = self.pipe(messages, **self.generation_args) 
            print(output[0]['generated_text'])

    def StartTextClassification(self, request, context):
        start_time = time.time()
        output = self.pipe(messages, **self.generation_args) 
        end_time = time.time()

        print(output)
        if self.debug:
            logging.info("Prompt output: " + output[0]['generated_text'])

        does_violate = "yes" in output.lower()
        response = tc_pb2.PromptResponse(doesViolate = does_violate)
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
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=16))
    tc_pb2_grpc.add_ClassifyTextServicer_to_server(ClassifyTextServicer(), server)
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
