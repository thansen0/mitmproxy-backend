import os
import grpc
import sys
import time
import signal
import accelerate
from concurrent import futures
import logging
import torch
#import tf_keras
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class ClassifyTextServicer(tc_pb2_grpc.ClassifyTextServicer):
    def __init__(self, empty_value=""):
        self.debug = True

        model_id = "Zyphra/Zamba2-7B"
        model_id = "Zyphra/Zamba2-2.7B"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id,
            # device_map="cuda",
            trust_remote_code=True,
            torch_dtype=torch.bfloat16
        )

        print("////////////////////////////////////////////////////")
        if self.debug:
            input_text = "What factors contributed to the fall of the Roman Empire?"
            input_ids = tokenizer(input_text, return_tensors="pt") #.to("cuda")

            outputs = model.generate(**input_ids, max_new_tokens=100)
            print(tokenizer.decode(outputs[0]))



        print("////////////////////////////////////////////////////")


    def StartTextClassification(self, request, context):
        start_time = time.time()
        output = self.model.generate(prompt=request.prompt, tokenizer=self.tokenizer, image_embeds=None, num_return_sequences=1)[0]
        end_time = time.time()

        if self.debug:
            logging.info("Prompt output: " + output)
            seconds_elapsed = end_time - start_time
            logging.info("Time to compute(s): "+str(seconds_elapsed))

        does_violate = "yes" in output.lower()
        response = tc_pb2.PromptResponse(doesViolate = does_violate)
        seconds_elapsed = end_time - start_time
        print("seconds: "+str(seconds_elapsed))

        return response

