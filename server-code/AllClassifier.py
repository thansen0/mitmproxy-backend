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
# pip install accelerate

sys.path.append("/protos")
import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc
import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc

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

class ClassifyImageServicer(ic_pb2_grpc.ClassifyImageServicer):
    def __init__(self):
        self.nsfw_model = predict.load_model("./mobilenet_v2_140_224/saved_model.h5")
        self.debug = True

    def StartClassification(self, request, context):
        cur_time = str(time.time())
        filename = ""

        # create file name
        try:
            filename = f"image_{cur_time}_path.{request.image.img_format}"
            filename = os.path.join("tmp-image", filename)
        except:
            logging.info("try block fail as file name is too big?")
            filename = f"image_{cur_time}_path.{request.image.img_format}"[:100]
            filename = os.path.join("tmp-image", filename)

        # run image file through classifier
        with open(filename, "wb") as f:
            f.write(request.image.data)
            
            try:
                classification = predict.classify(self.nsfw_model, filename)

                # classification results
                response = ic_pb2.ImageResponse(
                    drawings = classification[filename]['drawings'],
                    neutral = classification[filename]['neutral'],
                    porn = classification[filename]['porn'],
                    sexy = classification[filename]['sexy'],
                    hentai = classification[filename]['hentai'],
                )

            except Exception as e:
                logging.error(f"Can't classify image, exception: {e}")
                # not classified, allow image
                response = ic_pb2.ImageResponse(
                    drawings = 0.0,
                    neutral = 1.0,
                    porn = 0.0,
                    sexy = 0.0,
                    hentai = 0.0,
                )
                # normal safe image as an example
                # drawings: 0.014500734396278858
                # hentai: 0.024058302864432335
                # neutral: 0.9379702210426331
                # porn: 0.00865322258323431
                # sexy: 0.014817529357969761
                

        try:
            os.remove(filename)
            if self.debug:
                logging.info(f"The file {filename} has been deleted successfully.")
        except FileNotFoundError:
            logging.error(f"The file {filename} does not exist.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

        if self.debug:
            print("returning response: \n", response)

        return response

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
