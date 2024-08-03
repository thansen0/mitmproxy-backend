import os
import grpc
import sys
import time
import signal
from concurrent import futures
import logging
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class ClassifyTextServicer(tc_pb2_grpc.ClassifyTextServicer):
    def __init__(self):
        model_id = "vikhyatk/moondream2"
        revision = "2024-07-23"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, trust_remote_code=True, revision=revision
        )

        self.debug = True

        if self.debug:
            # output = self.model.generate(input_ids, max_length=5, num_return_sequences=1)
            output = self.model.generate(prompt="What is 2 + 2?", tokenizer=self.tokenizer, image_embeds=None, num_return_sequences=1, max_new_tokens=2)[0]
            logging.info("What is 2 + 2? " + output)

    def StartTextClassification(self, request, context):
        start_time = time.time()
        output = self.model.generate(prompt=request.prompt, tokenizer=self.tokenizer, image_embeds=None, num_return_sequences=1)[0]
        end_time = time.time()

        print(output)
        if self.debug:
            logging.info("Prompt output: " + output)

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
