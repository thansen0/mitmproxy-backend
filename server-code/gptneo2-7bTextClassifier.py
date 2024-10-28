import os
import grpc
import sys
import time
import signal
from concurrent import futures
import logging
# import torch
from transformers import pipeline
#from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class ClassifyTextServicer(tc_pb2_grpc.ClassifyTextServicer):
    def __init__(self):
        model_id = "EleutherAI/gpt-neo-2.7B"
        model_id = "EleutherAI/gpt-neo-1.3B"
        self.generator = pipeline('text-generation', model=model_id)
        oo = self.generator("Please set the next word in this sequence to be TRUE:", do_sample=True, min_length=50)
        print(oo)
        #self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        #self.model = AutoModelForCausalLM.from_pretrained(
        #    model_id
        #)

        self.debug = True

        print("///////////////////////////////////////////////")
        if self.debug:
            # output = self.model.generate(input_ids, max_length=5, num_return_sequences=1)
            output = self.generator("What is 2 + 2?", do_sample=True, min_length=50)
            # output = self.model.generate(prompt="What is 2 + 2?")
            logging.info("What is 2 + 2? " + output[0]["generated_text"])

            print("///////////////////////////////////////////////")

    def StartTextClassification(self, request, context):
        return
"""
        start_time = time.time()
        output = self.model.generate(prompt=request.prompt, tokenizer=self.tokenizer, do_sample=True, min_length=5)
        end_time = time.time()

        print(output)
        if self.debug:
            logging.info("Prompt output: " + output)

        does_violate = "yes" in output.lower()
        response = tc_pb2.PromptResponse(doesViolate = does_violate)
        seconds_elapsed = end_time - start_time
        print("seconds: "+str(seconds_elapsed))

        return response
"""

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
