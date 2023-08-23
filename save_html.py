from mitmproxy import http
import time
import logging
import pdb

def response(flow: http.HTTPFlow) -> None:
    # Check if the response contains HTML content

    cur_time = str(time.time())

    if "text/css" in flow.response.headers.get("content-type", ""):
        logging.info("text/css Response headers, no save: %s" % str(flow.response.headers.get("content-type")))

    elif "image/jpeg" in flow.response.headers.get("content-type", "") or "image/png" in flow.response.headers.get("content-type", ""):

        logging.info("image/jpeg Response headers: %s" % str(flow.response.headers.get("content-type", "")))
        # Save the HTML content to a file with a unique name
        filename = f"image_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.png"
        with open(filename, "wb") as f:
            f.write(flow.response.content)
        print(f"Saved Image content to {filename}")


    elif "text/html" in flow.response.headers.get("content-type", ""):
        logging.info("text/html Response headers: %s" % str(flow.response.headers.get("content-type", "")))
        # Save the HTML content to a file with a unique name
        tfilename = f"text_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.html"
        with open(tfilename, "wb") as f:
            f.write(flow.response.content)
        print(f"Saved HTML content to {tfilename}")

    elif "application/json" in flow.response.headers.get("content-type", ""):
        logging.info("text/html Response headers: %s" % str(flow.response.headers.get("content-type", "")))
        # Save the HTML content to a file with a unique name
        filename = f"json_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.html"
        with open(filename, "wb") as f:
            f.write(flow.response.content)
        print(f"Saved JSON content to {filename}")

    else:
        logging.info("else response headers: %s" % str(flow.response))

# Usage: mitmdump -s save_html.py
