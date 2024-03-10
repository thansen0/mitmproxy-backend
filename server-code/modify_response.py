from mitmproxy import http
import numpy as np
from urllib.parse import urlparse
import redis
import logging
import configparser
import json
import pdb
import re
import os
import io
import sys
import signal
from PIL import Image

import grpc
sys.path.append("/protos")
import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc

class ModifyResponse:
    def __init__(self):
        # define location of gRPC server
        self.server_ip_addr = "127.0.0.1"
        self.server_port_num = 50060

        # create gRPC channel connection
        self.channel = grpc.insecure_channel( self.server_ip_addr + ':' + str(self.server_port_num) )
        self.stub = ic_pb2_grpc.ClassifyImageStub(self.channel)

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
        content_filters_str = str(dynamic_config['CLIENT']['content_filters'])
        if content_filters_str.__eq__("NaN"):
            # if NaN, default to filter everything
            self.content_filters = "trans,lgbt,nsfw,atheism"

        self.content_filters = content_filters_str.split(',')
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
        if pretty_url is None:
            print("Issue with flow request url", flow)
            return False
        parsed_url = urlparse(pretty_url)

        # Collect all keys to check in a list
        keys_to_check = []

        # add keys to check for in redis, add to keys_to_check
        for filter_name in self.content_filters:
            # checks against root urls
            if filter_name in ['nsfw', 'genai', 'lgbt', 'atheism']:
                keys_to_check.append(f"{filter_name}:{parsed_url.netloc}".lower())
    
            # checks against reddit subs
            if "reddit.com/r/" in pretty_url:
                pattern = r"https?://(?:[\w\-]+\.)?reddit\.com/r/(\w+)/?"
                match = re.search(pattern, pretty_url)
                if match:
                    subreddit = match.group(1).lower()
                    if filter_name in ['nsfw', 'trans', 'lgbt', 'atheism']:
                        keys_to_check.append(f"{filter_name}:subreddit:{subreddit}".lower())

        #print("NEW FUNC: keys_to_check", keys_to_check)
        if keys_to_check:
            # send keys out to redis to check if they exist
            exists_count = self.ri.exists(*keys_to_check)
            #print("NEW FUNC: exists_count", exists_count)

            if exists_count > 0:
                # kill the connection since at least one value existed
                #print("NEW FUNC: banned site; exiting")
                return True

        return False

    def resize_image_bytes(self, image_bytes, new_size=(140, 224)):
        # Convert bytes data to a PIL Image object
        with Image.open(io.BytesIO(image_bytes)) as img:
            # Resize the image
            resized_img = img.resize(new_size)

            # Save the resized image to a bytes buffer
            img_byte_arr = io.BytesIO()
            resized_img.save(img_byte_arr, format=img.format)
            resized_img_bytes = img_byte_arr.getvalue()

        return resized_img_bytes

    def request(self, flow: http.HTTPFlow) -> None:
        request_str = str(flow.request) # i.e. GET reddit.com:80/full/url
        #logging.info(request_str)

        if self._url_exists(request_str, flow):
            flow.kill()
            #logging.info("Killed %s flow" % flow.request)



    def response(self, flow: http.HTTPFlow) -> None:
        if "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):
        # if "image" in flow.response.headers.get("content-type", ""):
            #logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type")))
            image_bytes = flow.response.content
            image_bytes = self.resize_image_bytes(image_bytes)

            # There are more formats than this but this is what we're going with
            img_format = "png"
            if "image/jpeg" in flow.response.headers.get("content-type", ""):
                img_format = "jpg"

            self.image = ic_pb2.NLImage(
                data=image_bytes,
                img_format="jpg"
            )

            request = ic_pb2.ImageMessage(
                image=self.image
            )
            #print("request build", request.image.img_format)
            response = self.stub.StartClassification(request)

            neutral_perc = response.neutral # neutral if near 1
            drawings_perc = response.drawings # porn if near 1
            porn_perc = response.porn # porn if near 1
            sexy_perc = response.sexy # sexy if near 1
            hentai_perc = response.hentai # hentai if near 1

            if neutral_perc < 0.5 or porn_perc > 0.5 or hentai_perc > 0.5:
                #logging.info("filling; neutral %f, porn %f, hentai %f", neutral_perc, porn_perc, hentai_perc)
                # NSFW image, replace with fill
                #fill_image_path = "./fill.svg"
                fill_image_path = "./fill.png"
                with open(fill_image_path, "rb") as file:
                    file_bytes = file.read()
                flow.response.content = file_bytes


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
