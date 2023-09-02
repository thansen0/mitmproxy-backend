from mitmproxy import ctx, http
import numpy as np
from CustomList import CustomList
from nsfw_detector import predict
import logging
import time
import json
import pdb
import os

class ModifyResponse:
    def __init__(self):
        # load model
        self.nsfw_model = predict.load_model("./mobilenet_v2_140_224/saved_model.h5")
        # Create watch list
        self.watch_list = CustomList("mixed_use.txt")


    def request(self, flow: http.HTTPFlow) -> None:
        #breakpoint()
        host = flow.request.headers[b'host']
        #full_url = flow.request.headers[b'Referer']
        #print("full url: ", full_url)

        if "thomashansen.xyz" in host:
            if "/blog/" in str(flow.request):
                flow.kill()
                logging.info("Killed %s flow" % flow.request)


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
                neutral_perc = classification[filename]['neutral'] # not porn if near 1
                porn_perc = classification[filename]['porn'] # porn if near 1
                sexy_perc = classification[filename]['sexy'] # sexy if near 1
                hentai_perc = classification[filename]['hentai'] # hentai if near 1

                if neutral_perc < 0.7 or porn_perc > 0.7 or hentai_perc > 0.7:
                    logging.info("neutral %d, porn %d, hentai %d", neutral_perc, porn_perc, hentai_perc)
                    # NSFW image, replace with fill
                    fill_image_path = "./fill.jpeg"
                    with open(fill_image_path, "rb") as file:
                        file_bytes = file.read()
                    flow.response.content = file_bytes

                # delete image
                os.remove(filename)


#        elif "application/json" in flow.response.headers.get("content-type", ""):
#            if flow.response.status_code >= 200 or flow.response.status_code < 300:
#                if "reddit.com" in flow.response.headers.get('host', ''):
#                    raw_json = flow.response.content
#                    input_json = json.loads(raw_json)

addons = [ModifyResponse()]

