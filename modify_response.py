from mitmproxy import ctx, http
import time
import numpy as np
from CustomList import CustomList
import pdb
import logging

class ModifyResponse:
    def __init__(self):
        self.num = 0

        # Create watch list
        self.watch_list = CustomList("mixed_use.txt")

    def response(self, flow: http.HTTPFlow) -> None:

        cur_time = str(time.time())

        if "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):
            logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type")))
            # Save the HTML content to a file with a unique name
            filename = f"image_original_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.png"
            with open(filename, "wb") as f:
                f.write(flow.response.content)
            # print(f"Saved Image content to {filename}")

            fill_image_path = "./fill.jpeg"
            with open(fill_image_path, "rb") as file:
                file_bytes = file.read()
            flow.response.content = file_bytes

            




addons = [ModifyResponse()]

