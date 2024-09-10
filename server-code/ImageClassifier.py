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
