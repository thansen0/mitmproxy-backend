import grpc
from concurrent import futures
import sys
from PIL import Image

sys.path.append("/protos")
import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc

# This serves as a server you can use to test whether the client is
# operational and sending the data as we expect
class ClassifyImageServicer(ic_pb2_grpc.ClassifyImageServicer):
    def StartClassification(self, request, context):
        # create file name
        try:
            filename = f"image_filename"
            filename = os.path.join("tmp-image", filename)
        except:
            # KeyError(key)
            logging.info("error")
            filename = f"image_original_{cur_time}_path_{flow.request.path.replace('/', '_')}"[:100]
            filename = os.path.join("tmp-image", filename)

        # run image file through classifier
        with open(filename, "wb") as f:
            f.write(request.image.data)
            classification = predict.classify(self.nsfw_model, filename)

        # Your server logic here
            response = ic_pb2.ConnectionResp(
                drawings = classification[filename]['neutral'],
                neutral = classification[filename]['neutral'],
                porn = classification[filename]['porn'],
                sexy = classification[filename]['sexy'],
                hentai = classification[filename]['hentai'],
            )

        # delete image 
        print("returning response: ", response)
        return response

def run_server():
    port_num = "50059"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    ic_pb2_grpc.add_ClassifyImageServicer_to_server(ClassifyImageServicer(), server)
    server.add_insecure_port("[::]:" + port_num)
    print("starting server on port " + port_num)
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    run_server()
