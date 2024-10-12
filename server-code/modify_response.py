from mitmproxy import http
import numpy as np
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
import redis
import logging
import configparser
import pdb
import re
import os
import io
import sys
import json
import signal
from PIL import Image
from bs4 import BeautifulSoup
import concurrent.futures
from datetime import datetime
import pytz
import pdb

import grpc
sys.path.append("/protos")
import protos.image_classification_pb2 as ic_pb2
import protos.image_classification_pb2_grpc as ic_pb2_grpc

import protos.text_binary_classification_pb2 as tc_pb2
import protos.text_binary_classification_pb2_grpc as tc_pb2_grpc

class ModifyResponse:
    def __init__(self):
        # define location of gRPC server
        self.server_ip_addr = "127.0.0.1"
        self.server_port_num = 50060
        self.groq_port_num = 50061

        # create gRPC channel connection for images
        img_channel = grpc.insecure_channel(f"{self.server_ip_addr}:{str(self.server_port_num)}" )
        self.stub = ic_pb2_grpc.ClassifyImageStub(img_channel)

        # create gRPC channel connection for Groq
        groq_channel = grpc.insecure_channel(f"{self.server_ip_addr}:{str(self.groq_port_num)}" )
        self.groq_stub = tc_pb2_grpc.ClassifyTextStub(groq_channel)

        # config file loading
        config = configparser.ConfigParser()
        config.read('redis-config.ini')

        # Get Redis connection information
        self.redis_host = config['REDIS']['redis_host']
        self.redis_port = int(config['REDIS']['redis_port'])
        self.redis_auth = config['REDIS']['redis_auth']
        self.redis_db = int(config['REDIS']['redis_db'])

        # this should all become a bitmask someday
        self.site_filters = ['nsfw', 'genai', 'trans', 'lgbt', 'atheism', 'drug', 'weed', 'tobacco', 'alcohol', 'shortvideo', 'gambling', 'communism', 'socialism']
        self.subreddit_filters = ['nsfw', 'trans', 'lgbt', 'atheism', 'drug', 'weed', 'tobacco', 'alcohol', 'antiwork', 'antiparent', 'shortvideo', 'gambling', 'suicide', 'nonmonogamy', 'communism', 'socialism', 'misogyny']

        # config file loading
        dynamic_config = configparser.ConfigParser()
        dynamic_config.read('config.ini')
        content_filters_str = str(dynamic_config['CLIENT']['content_filters'])
        if content_filters_str.__eq__("NaN"):
            # if NaN, default to filter everything
            self.content_filters = "trans,lgbt,nsfw,atheism,drug,weed,alcohol,tobacco,antiparent,safesearch,nonmonogamy,suicide,gambling,communism,socialism"

        self.content_filters = content_filters_str.split(',')
        logging.info(f"Content Filters: {self.content_filters}")

        # Connect to Redis
        try:
            self.ri = redis.StrictRedis(host=self.redis_host, port=self.redis_port, db=self.redis_db, password=self.redis_auth, decode_responses=True)
            logging.info("Connected to Redis")
        except Exception as e:
            logging.error(f"Error connecting to Redis: {e}")
            exit(1)

        # Support:
        # America/Chicago CT
        # America/Los_Angeles PT
        # America/New_York ET
        # America/Denver MT
        # America/Anchorage # observes daylight savings
        # America/Adak # doesn't observe daylight savings
        # Pacific/Honolulu
        self.timezone = str(dynamic_config['CLIENT']['timezone'])
        self.time_schedule = str(dynamic_config['CLIENT']['time_schedule'])
        # this function will change them to empty if they're poorly formated 
        self.set_timezone_and_schedule(self.timezone, self.time_schedule)


    def _url_exists(self, flow, pretty_url):
        # recursive calls may already have a parsed url
        if not pretty_url:
            pretty_url = flow.request.pretty_url
            if pretty_url is None:
                logging.error("Issue with flow request url", flow)
                return False
            parsed_url = urlparse(pretty_url)
        else:
            parsed_url = urlparse(pretty_url)

        # Collect all redis keys to check
        keys_to_check = []

        # TODO move filter for loop off of O(n) time
        # add keys to check for in redis, add to keys_to_check
        for filter_name in self.content_filters:
            # checks against root urls, only check if there is a url filter
            if filter_name in self.site_filters:
                keys_to_check.append(f"{filter_name}:{parsed_url.netloc}".lower())
    
            # checks against reddit subs
            if "reddit.com/r/" in pretty_url:
                pattern = r"https?://(?:[\w\-]+\.)?reddit\.com/r/(\w+)/?"
                match = re.search(pattern, pretty_url)
                if match:
                    subreddit = match.group(1).lower()
                    # only check if there is a reddit sub filter
                    if filter_name in self.subreddit_filters:
                        keys_to_check.append(f"{filter_name}:subreddit:{subreddit}".lower())

            if "shortvideo" == filter_name and "youtube.com/shorts" in pretty_url:
                # kill shorts
                return True

        if keys_to_check:
            # send keys out to redis to check if they exist
            exists_count = self.ri.exists(*keys_to_check)

            if exists_count > 0:
                # kill the connection since at least one value existed
                return True

        return False

    def _response_url_exists(self, flow, pretty_url):
        parsed_url = ""

        if not hasattr(flow, "response"):
            # no response field, can quit
            return

        # TODO not used, can remove
        # recursive calls may already have a parsed url
        if not pretty_url:
            pretty_url = flow.request.pretty_url
            if pretty_url is None:
                print("Issue with flow request url", flow)
                return False
            parsed_url = urlparse(pretty_url)
        else:
            parsed_url = urlparse(pretty_url)

        encoding = self.get_encoding(flow)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self.process_yandex, flow, pretty_url, encoding),
                executor.submit(self.process_google, flow, pretty_url, encoding),
                executor.submit(self.process_reddit, flow, pretty_url, encoding),
                executor.submit(self.process_mastodon, flow, pretty_url, encoding)
            ]
            # Wait for all threads to complete (optional, depending on your use case)
            concurrent.futures.wait(futures)

    # returns true if the kid can be on the internet
    # in limit means within allowed limit
    def _in_time_limit(self):
        return True
#        if self.timezone == "" or self.time_schedule == None:
#            return True

#        current_time = datetime.now(self.timezone)
#        current_hour = str(current_time.hour)
#        current_day = str(current_time.weekday()) # Monday == 0, Sunday == 6
        
#        return self.time_schedule[current_day][current_hour]

    def _if_safe_search(self, flow):
        if "safesearch" in self.content_filters:
            search_engines = {
                "google.com": {"safe": "active"},
                "bing.com": {"adlt": "strict"},
                "yandex.com": {"family": "yes"},
                "duckduckgo.com": {"kp": "1"},
                "search.yahoo.com": {"vm": "r"},
                "ask.com": {"safeSearch": "on"},
                "search.aol.com": {"safeSearch": "on"},
                "baidu.com": {"filter": "1"},
                "youtube.com": {"sp": "EgIQAQ%3D%3D"},
                "flickr.com": {"safe_search": "1"},
                "vimeo.com": {"filter": "cc"},
                "reddit.com": {"include_over_18": "off"},
                "twitter.com": {"safe": "1"},
                "x.com": {"safe": "1"},
                "pinterest.com": {"no_safe_search": "false"}
            }

            # Parse the URL
            url = urlparse(flow.request.url)
            query_params = parse_qs(url.query)
            new_url = ""

            # Check if the request URL matches any of the search engines
            for engine, params in search_engines.items():
                if engine in url.netloc:
                    # Update the query parameters with the safe search parameters
                    query_params.update(params)
                    # Rebuild the URL with the modified query parameters
                    new_query = urlencode(query_params, doseq=True)
                    new_url = urlunparse((url.scheme, url.netloc, url.path, url.params, new_query, url.fragment))
                    break

            return new_url

        return None

    def process_yandex(self, flow, pretty_url, encoding):
        if ("yandex.com/search/?text" in pretty_url):
            soup = BeautifulSoup(flow.response.content, features="html.parser")
            for li in soup.find_all("li", class_="serp-item serp-item_card"):
                # Find the <a> which contains the outbound link <li>
                aref = li.find("a", class_="OrganicTitle-Link", href=True) # more classes: Path-Item link path__item link organic__greenurl
                if aref:
                    #print("YANDEX search url: ", aref['href'])
                    # if the url exists in redis, remove
                    if self._url_exists(flow, aref['href']):
                        li.decompose()

            # add back modified soup content
            modified_content = str(soup).encode(encoding)
            flow.response.content = modified_content


    def process_google(self, flow, pretty_url, encoding):
        if ("google.com/search?" in pretty_url) and ("text/html" in flow.response.headers.get("content-type", "")):
            soup = BeautifulSoup(flow.response.content, features="html.parser")
            # parse link search
            for li in soup.find_all("div", class_="MjjYud"):
                # Find the <a> which contains the outbound link <li>
                aref = li.find("a", href=True, attrs={'jsname': 'UWckNb'})
                if aref:
                    # if true, remove
                    if self._url_exists(flow, aref['href']):
                        li.decompose()

            # add back modified soup content
            modified_content = str(soup).encode(encoding)
            flow.response.content = modified_content

    def process_reddit(self, flow, pretty_url, encoding):
        if ("reddit.com/svc/shreddit/feeds" in pretty_url) or ("reddit.com/r/all" in pretty_url) or ("reddit.com/r/popular" in pretty_url):
            soup = BeautifulSoup(flow.response.content, features="html.parser")
            # parse link search
            for article in soup.find_all("article"):
                post_menu = article.find("shreddit-post-overflow-menu")
                if post_menu:
                    reddit_post_url = "https://www.reddit.com" + post_menu['permalink']

                    # if true, remove
                    if self._url_exists(flow, reddit_post_url):
                        # print("POST URL being decomposed: ", reddit_post_url)
                        article.decompose()

            # add back modified soup content
            modified_content = str(soup).encode(encoding)
            flow.response.content = modified_content

    # not only untested, but this may not be how it gets data
    def process_mastodon(self, flow, pretty_url, encoding):
        # logging.info(f"MASTODON pretty url: {pretty_url}")
        if "mastodon.social/api/v1/trends/statuses" in pretty_url and ("application/json" in flow.response.headers.get("content-type", "")):
            logging.info(f"Inside MASTODON if statement")

            data = []
            filtered_data = []
            try:
                data = json.loads(flow.response.content)
                logging.info(f"Inside MASTODON if statement, loaded data ")
                # print(f"{data}")
            except Exception as e:
                logging.error(f"HELP Failed to load json data for MASTODON link, exiting. Exception: str(e)")
                return # empty retun

            logging.info("About to start threadpool SINGLE FUNC")
            # Initialize a ThreadPoolExecutor
            #classify_status(data)
            try:
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    # Map the classify_status function to each item in the data
                    logging.info(f"About to start map {len(data)}")
                    # logging.info(f"{data[0]}")
                    filtered_data = list(executor.map(self.classify_status, data))
            except Exception as e:
                logging.error(f"Unhandled exception in ThreadPoolExecutor: {e}")

            logging.info(f"Size of data: {len(data)}")
            logging.info(f"Size of pre-filtered data: {len(filtered_data)}")
            filtered_data = [item for item, rr in zip(data, filtered_data) if rr]
            logging.info(f"Size of data: {len(data)}")
            logging.info(f"Size of filtered data: {len(filtered_data)}")
            ## this makes no sense here? modified_content = str(soup).encode(encoding)
            flow.response.content = json.dumps(filtered_data)

    def classify_status(self, status):
        logging.info("INSIDE classify_status function. ")

        #if status['content']:
        if status.get('content', status.get('note')):
            try:
                # TODO This is still replying with a long response for too many posts
                prompt_text = f"You are a fast AI bot tasked with quickly classifying text content on whether it supports a certain ideology. Please answer the following question with either a YES or NO. Does the following tweet explicitly discuss [{self.content_filters}] favorable? \"{status.get('content', status.get('note'))}\". Remember: only reply with a YES or a NO. Reply YES if the post explicitly discusses any of the mentioned topics."

                # I could get a significant speed increase by passing in
                # multiple prompts at a time, groq can handle it
                request = tc_pb2.PromptMessage(
                    prompt=prompt_text
                )

                response = self.groq_stub.StartTextClassification(request)
                if response.doesViolate:
                    logging.info(f"{response.doesViolate} doesViolate is TRUE, removing from feed.")
                else:
                    # only add to filtered_data if we want to keep the post
                    #logging.info(f"status: {status}, status[content]: {status.get('content')}")
                    logging.info(f"{response.doesViolate} doesViolate is FALSE, staying in feed.")
                    return status

            except grpc.RpcError as e:
                logging.error(f"gRPC error: {e.details()}")
                status_code = e.code()
                logging.error(f"gRPC status code value: {status_code.value}")
                # add post if gRPC isn't working
                # filtered_data.append(status)
                return status

            except Exception as e:
                logging.error("An error occurred:", str(e))
                # add post if it encounters a generic error
                # filtered_data.append(status)
                return status
        else:
            logging.error("classify_status: No content on TEXT Classification")

        # removing from feed
        return ""

    def get_encoding(self, flow):
        default_encoding = 'utf-8'
        # Extract the Content-Type header
        content_type = flow.response.headers.get('Content-Type', '')
    
        # Attempt to parse the charset (encoding) from the Content-Type header
        parts = content_type.split(';')
        encoding = default_encoding
        for part in parts:
            if 'charset=' in part:
                encoding = part.split('=')[1].strip()
                break

        return encoding

    def set_timezone_and_schedule(self, timezone, schedule):
        try:
            self.timezone = pytz.timezone(str(timezone))

            schedule = schedule.replace("True", "true")
            schedule = schedule.replace("False", "false")
            schedule = schedule.replace("'", '"')

            self.time_schedule = json.loads(schedule)

            for d in range(0, 6):
                for h in range(0, 23):
                    if None == self.time_schedule[str(d)][str(h)]:
                        logging.error("Found None value in time schedule, which is bad ", d, ":", h)

            logging.info("Timezone and schedule successfully added.")
            return True

        except:
            logging.error("Time schedule not set up or encountered an  error. " + timezone)
            self.timezone = ""
            self.time_schedule = None
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
        # TODO consider creating a whitelist of urls:
        # update.googleapis.com # used for safe browsing data/etc in chrome
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(self._url_exists, flow, None),
                executor.submit(self._if_safe_search, flow),
                executor.submit(self._in_time_limit)
            ]

            if not futures[2].result():
                futures[0].cancel()
                futures[1].cancel()
                logging.info("_in_time_limit failed, killing connection")
                # not in time limit, stop 
                # flow.kill()
                end_of_sched = urlparse("https://www.parentcontrols.win/time_limit_reached")
                # TODO should I just assign the string?
                if "parentcontrols.win" not in flow.request.url:
                    flow.request.url = urlunparse(end_of_sched)

            elif futures[0].result():
                futures[1].cancel()
                futures[2].cancel()
                logging.info("_url_exists triggered, killing connection")
                flow.kill()
            else:
                futures[0].cancel()
                futures[2].cancel()
                new_url = futures[1].result()
                parsed_url = urlparse(new_url)
                if all([parsed_url.scheme, parsed_url.netloc]):  # Check if URL is valid
                    flow.request.url = urlunparse(parsed_url)
                #else:
                    #logging.error(f"Invalid request URL, remains unchanged: {new_url}")
                    # url remains unchanged
    

    def response(self, flow: http.HTTPFlow) -> None:
        if "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):
        # if "image" in flow.response.headers.get("content-type", ""):
            #logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type")))
            image_bytes = flow.response.content

            try:
                image_bytes = self.resize_image_bytes(image_bytes)
            except Exception as e:
                logging.error(f"Failure to resize image, {str(e)}. Image path {str(flow.request.url)}")
                # finish response, don't do anything
                return

            # There are more formats than this but this is what we're going with
            image_format = "png"
            if "image/jpeg" in flow.response.headers.get("content-type", ""):
                image_format = "jpg"

            self.image = ic_pb2.NLImage(
                data=image_bytes,
                img_format=image_format
            )

            request = ic_pb2.ImageMessage(
                image=self.image
            )
            #print("request build", request.image.img_format)
            response = self.stub.StartClassification(request)

            neutral_perc = response.neutral # neutral if near 1
            # drawings_perc = response.drawings # porn if near 1
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

        else:
            self._response_url_exists(flow, None)

    def close(self):
        if self.ri:
            self.ri.connection_pool.disconnect()
        logging.info("redis is closed")

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

