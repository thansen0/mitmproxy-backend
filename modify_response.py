from mitmproxy import ctx, http
import time
import numpy as np
from CustomList import CustomList
from nsfw_detector import predict
import logging
import json
import pdb

class ModifyResponse:
    def __init__(self):
        # load model
        self.nsfw_model = predict.load_model("./mobilenet_v2_140_224/saved_model.h5")
        # Create watch list
        self.watch_list = CustomList("mixed_use.txt")


    def response(self, flow: http.HTTPFlow) -> None:
        cur_time = str(time.time())

        if "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):
            logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type")))
            # Save the HTML content to a file with a unique name
            filename = f"image_original_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}"
            with open(filename, "wb") as f:
                f.write(flow.response.content)
                #breakpoint()

                classification = predict.classify(self.nsfw_model, filename)
                logging.info(classification)

                # may not be filename, check log
                neutral_perc = classification[filename]['neutral']
                if neutral_perc > 0.8:
                    # NSFW image, replace with fill
                    fill_image_path = "./fill.jpeg"
                    with open(fill_image_path, "rb") as file:
                        file_bytes = file.read()
                    flow.response.content = file_bytes


        elif "application/json" in flow.response.headers.get("content-type", ""):

            if flow.response.status_code >= 200 or flow.response.status_code < 300:
                if "reddit.com" in flow.response.headers.get('host', ''):
                    raw_json = flow.response.content
                    input_json = json.loads(raw_json)

addons = [ModifyResponse()]

