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

class ClassifyTextServicer(tc_pb2_grpc.ClassifyTextServicer):
    def __init__(self, groq_api_key):
        self.debug_img = False
        self.debug_txt = True

        print("GROQ api key: "+ str(groq_api_key))
        self.client = Groq(
            api_key=groq_api_key,
        )


    def StartTextClassification(self, request, context):
        if self.debug_txt:
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

        if self.debug_txt:
            print(output)
            logging.info("Prompt output: " + chat_completion.choices[0].message.content)

        does_violate = "yes" in output.lower()
        response = tc_pb2.PromptResponse(doesViolate=does_violate)

        if self.debug_txt:
            seconds_elapsed = end_time - start_time
            print("seconds: "+str(seconds_elapsed))

        return response
