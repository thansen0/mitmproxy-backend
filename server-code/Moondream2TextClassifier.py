import os
import grpc
import sys
import time
import signal
import accelerate
from concurrent import futures
import logging
import torch
# import tf_keras
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers import GPTJForCausalLM
from PIL import Image

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class ClassifyTextServicer(tc_pb2_grpc.ClassifyTextServicer):
    def __init__(self, empty_value=""):
        self.debug = True

        model_id = "vikhyatk/moondream2"
        revision = "2024-08-26"
        self.tokenizer = AutoTokenizer.from_pretrained(model_id, revision=revision)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_id, trust_remote_code=True, revision=revision
        )

        self.tokenizer = AutoTokenizer.from_pretrained(model_id, return_tensors="pt")

        if self.debug:
            image = Image.new("RGB", (1, 1))
            #image = Image.open("./fill.png")
            enc_image = self.model.encode_image(image)
            print(self.model.answer_question(enc_image, "Could you describe this image?", self.tokenizer))

        logging.info("Model {model_id} initialized")



    def StartTextClassification(self, request, context):
        start_time = time.time()

        # TODO I should accept a picture through the request
        image = Image.new("RGB", (1, 1)) # empty image
        enc_image = self.model.encode_image(image)
        output = self.model.answer_question(enc_image, "{request.prompt}", self.tokenizer)

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

