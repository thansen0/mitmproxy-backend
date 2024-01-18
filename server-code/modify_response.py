from mitmproxy import http
import numpy as np
from nsfw_detector import predict
from urllib.parse import urlparse
import redis
import logging
import configparser
import time
import json
import pdb
import re
import os
import signal

class ModifyResponse:
    def __init__(self):
        # load model
        self.nsfw_model = predict.load_model("./mobilenet_v2_140_224/saved_model.h5")

        # config file loading
        config = configparser.ConfigParser()
        config.read('redis-config.ini')

        # Get Redis connection information
        self.redis_host = config['REDIS']['redis_host']
        self.redis_port = int(config['REDIS']['redis_port'])
        self.redis_auth = config['REDIS']['redis_auth']
        self.redis_db = int(config['REDIS']['redis_db'])

        # config file loading
        dynamic_config = configparser.ConfigParser()
        dynamic_config.read('config.ini')
        self.content_filters = str(dynamic_config['CLIENT']['content_filters'])
        if self.content_filters.__eq__("NaN"):
            # if NaN, default to filter everything
            self.content_filters = "trans,lgbt,nsfw"
        print("Content Filters:", self.content_filters)

        # Connect to Redis
        try:
            self.ri = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_auth, decode_responses=True)
            print("Connected to Redis")
        except Exception as e:
            print(f"Error connecting to Redis: {e}")
            exit(1)

    def _url_exists(self, url, flow):

        pretty_url = flow.request.pretty_url
        if pretty_url == None:
            print("Issue with flow request url", flow)
            return False
        parsed_url = urlparse(pretty_url)
        print("pretty_url: ",pretty_url)
        #print("parsed_url:", parsed_url)

        # checks if it's a porn link, always blocked
        if "nsfw" in self.content_filters:
            url_key = "nsfw:" + parsed_url.netloc
            if self.ri.exists(url_key):
                # This should kill the connection
                return True

        # Define a regex pattern to extract the domain and subreddit
        if "reddit.com/r/" in pretty_url:
            print("ABOUT TO Start regex matching")
            #pattern = r"/r/([^/]+)/"
            pattern = r"https?://(?:[\w\-]+\.)?reddit\.com/r/(\w+)/?"    

            match = re.search(pattern, pretty_url)            
            if match:
                # Extract the domain and subreddit from the match object
                # domain = match.group(0)  # /r/subreddit/
                subreddit = match.group(1)  # just "subreddit" part
                logging.info("REDDIT subreddit: %s", subreddit)

                # checks if this is nsfw sub
                if "nsfw" in self.content_filters:
                    url_key = f'nsfw:subreddit:{subreddit}'.lower()
                    logging.info("SUBREDDIT url_key: %s", url_key)
                    if self.ri.exists(url_key):
                        return True

                # checks if this is a pro-trans sub
                if "trans" in self.content_filters:
                    url_key = f'trans:subreddit:{subreddit}'.lower()
                    if self.ri.exists(url_key):
                        return True

                # checks if this is a pro-lgbt sub
                if "lgbt" in self.content_filters:
                    url_key = f'lgbt:subreddit:{subreddit}'.lower()
                    if self.ri.exists(url_key):
                        return True

            return False

        #logging.info("Reddit is not in URL")
        return False

    def request(self, flow: http.HTTPFlow) -> None:
        #breakpoint()
        #host = flow.request.headers[b'host'] # i.e. reddit.com
        #full_url = flow.request.headers[b'Referer']
        #print("full url: ", full_url)
        #logging.info(flow.request)
        # print("host: ", host)

        request_str = str(flow.request) # i.e. GET reddit.com:80/full/url
        logging.info(request_str)

        if self._url_exists(request_str, flow):
            flow.kill()
            logging.info("Killed %s flow" % flow.request)



    def response(self, flow: http.HTTPFlow) -> None:
        cur_time = str(time.time())

        if "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):
        # if "image" in flow.response.headers.get("content-type", ""):
            #logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type")))
            # Save the HTML content to a file with a unique name
            # filename = f"image_original_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}"
            try:
                filename = f"image_original_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}"
                filename = os.path.join("tmp-image", filename)
            except:
                # KeyError(key)
                logging.info("Couldn't get host from flow.request.host")
                filename = f"image_original_{cur_time}_path_{flow.request.path.replace('/', '_')}"[:100]
                filename = os.path.join("tmp-image", filename)

            with open(filename, "wb") as f:
                f.write(flow.response.content)
                classification = predict.classify(self.nsfw_model, filename)

                # may not be filename, check log
                neutral_perc = classification[filename]['neutral'] # not porn if near 1
                porn_perc = classification[filename]['porn'] # porn if near 1
                sexy_perc = classification[filename]['sexy'] # sexy if near 1
                hentai_perc = classification[filename]['hentai'] # hentai if near 1

                if neutral_perc < 0.5 or porn_perc > 0.5 or hentai_perc > 0.5:
                    logging.info("filling; neutral %d, porn %d, hentai %d", neutral_perc, porn_perc, hentai_perc)
                    # NSFW image, replace with fill
                    #fill_image_path = "./fill.svg"
                    fill_image_path = "./fill.png"
                    with open(fill_image_path, "rb") as file:
                        file_bytes = file.read()
                    flow.response.content = file_bytes

                # delete image
                os.remove(filename)

    def close(self):
        if self.ri:
            self.ri.connection_pool.disconnect()
        print("redis is closed")

    def __del__(self):
        self.close()

# make sure to close redis connection
def signal_handler(sig, frame):
    try:
        addons[0].close()
    except:
        addons.close()
    exit(0)

addons = [ModifyResponse()]

# Register signal handler for SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, signal_handler)
