import os
import grpc
import sys
import time
import signal
from PIL import Image
from concurrent import futures
import logging
from nsfw_detector import predict

sys.path.append("/protos")
import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
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
            # KeyError(key)
            logging.info("try block fail as file name is too big?")
            filename = f"image_{cur_time}_path.{request.image.img_format}"[:100]
            filename = os.path.join("tmp-image", filename)

        # run image file through classifier
        with open(filename, "wb") as f:
            f.write(request.image.data)
            classification = predict.classify(self.nsfw_model, filename)

            # Your server logic here
            response = ic_pb2.ImageResponse(
                drawings = classification[filename]['drawings'],
                neutral = classification[filename]['neutral'],
                porn = classification[filename]['porn'],
                sexy = classification[filename]['sexy'],
                hentai = classification[filename]['hentai'],
            )

        # delete image
        try:
            os.remove(filename)
            print(f"The file {filename} has been deleted successfully.")
        except FileNotFoundError:
            print(f"The file {filename} does not exist.")
        except Exception as e:
            print(f"An error occurred: {e}")

        if self.debug:
            print("returning response: ", response)

        return response

def signal_handler(sig, frame):
    print("Ctrl-C pressed. Cleaning up and exiting.")
    # Perform any necessary cleanup here
    sys.exit(0)

def run_server():
    port_num = "50060"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=16))
    ic_pb2_grpc.add_ClassifyImageServicer_to_server(ClassifyImageServicer(), server)
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
