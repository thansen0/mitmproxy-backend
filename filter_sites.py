from mitmproxy import ctx, http
import time
import numpy as np
from CustomList import CustomList
import pdb

class CustomDomainFilter:
    def __init__(self):
#        pdb.set_trace()
        self.num = 0

        # Create watch list
        self.watch_list = CustomList("mixed_use.txt")

        # print(self.watch_list)

    def request(self, flow: http.HTTPFlow) -> None:
        print(http.HTTPFlow)

        requested_domain = flow.request.host.lower()

        # Check if the requested domain should be proxied
        if self.watch_list.in_list(requested_domain):
            ctx.log.info(f"Proxying: {requested_domain}")
            flow.request.host = "proxy.example.com"  # Set the proxy host
            flow.request.port = 8080  # Set the proxy port
        else:
            ctx.log.info(f"Bypassing: {requested_domain}")
            flow.kill()


#    def processResponse("domain"):
#        # Check if the response contains HTML content
#        if "image/jpeg" or "image/png" in flow.response.headers.get("content-type", ""):
#            # Save the HTML content to a file with a unique name
#            cur_time = str(time.time())
#            filename = f"html_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.png"
#            with open(filename, "wb") as f:
#                f.write(flow.response.content)
#            print(f"Saved HTML content to {filename}")
#
#            self.num = self.num + 1
#            flow.response.headers["count"] = str(self.num)

addons = [CustomDomainFilter()]





#def response(flow: http.HTTPFlow) -> None:
#    # Check if the response contains HTML content
#    if "text/html" in flow.response.headers.get("content-type", ""):
#        # Save the HTML content to a file with a unique name
#        cur_time = str(time.time())
#        filename = f"html_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.html"
#        #with open(filename, "wb") as f:
#        with open(filename, "a") as f:
#            f.write(flow.response.content)
#        print(f"Saved HTML content to {filename}")

# Usage: mitmdump -s filter_sites.py
