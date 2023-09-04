from mitmproxy import ctx, http
import numpy as np
from CustomList import CustomList
from nsfw_detector import predict
import redis
import logging
import time
import json
import pdb
import re
import os

class ModifyResponse:
    def __init__(self):
        # load model
        self.nsfw_model = predict.load_model("./mobilenet_v2_140_224/saved_model.h5")
        # Create watch list
        self.watch_list = CustomList("mixed_use.txt")


        # Create a Redis connection
        self.redis_host = 'localhost'  # Replace with your Redis server's hostname or IP address
        self.redis_port = 6379         # Replace with your Redis server's port
        self.redis_db = 0              # Replace with your desired Redis database number (default is 0)

        # Connect to Redis
        try:
            self.ri = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db, decode_responses=True)
            print("Connected to Redis")
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            exit(1)

    def _url_exists(self, url):
        # perform modifications to url if needed
        # Define a regex pattern to extract the domain and subreddit


        print("The URL passed in:"+url)
        if "reddit.com" in url:
            logging.info("This is a reddit URL")
            pattern = r'https?://(www\.)?reddit\.com/r/([^/]+)/'
    
            match = re.search(pattern, url)            
            if match:
                # Extract the domain and subreddit from the match object
                domain = match.group(0)  # Full matched URL
                subreddit = match.group(2)  # Subreddit part

                # url_key = f'reddit.com/r/{subreddit}/'.lower()
                url_key = subreddit.lower()

                return self.ri.exists(url_key)

            logging.info("Reddit in URL but match failed")
            return False

        logging.info("Reddit is not in URL")

        return False

    def request(self, flow: http.HTTPFlow) -> None:
        #breakpoint()
        host = flow.request.headers[b'host'] # i.e. reddit.com
        #full_url = flow.request.headers[b'Referer']
        #print("full url: ", full_url)
        logging.info(flow.request)
        # print("host: ", host)

        request_str = str(flow.request) # i.e. GET reddit.com:80/full/url
        logging.info(request_str)

        if self._url_exists(request_str):
            flow.kill()
            logging.info("Killed %s flow" % flow.request)



    def response(self, flow: http.HTTPFlow) -> None:
        cur_time = str(time.time())

        #if "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):
        if "image" in flow.response.headers.get("content-type", ""):
            #logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type")))
            # Save the HTML content to a file with a unique name
            filename = f"image_original_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}"
            with open(filename, "wb") as f:
                f.write(flow.response.content)
                #breakpoint()

                classification = predict.classify(self.nsfw_model, filename)
                # logging.info(classification)

                # may not be filename, check log
                neutral_perc = classification[filename]['neutral'] # not porn if near 1
                porn_perc = classification[filename]['porn'] # porn if near 1
                sexy_perc = classification[filename]['sexy'] # sexy if near 1
                hentai_perc = classification[filename]['hentai'] # hentai if near 1

                if neutral_perc < 0.5 or porn_perc > 0.5 or hentai_perc > 0.5:
                    logging.info("filling; neutral %d, porn %d, hentai %d", neutral_perc, porn_perc, hentai_perc)
                    # NSFW image, replace with fill
                    fill_image_path = "./fill.jpeg"
                    with open(fill_image_path, "rb") as file:
                        file_bytes = file.read()
                    flow.response.content = file_bytes

                # delete image
                os.remove(filename)


addons = [ModifyResponse()]

