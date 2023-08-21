# save_html.py

from mitmproxy import http
import time

def response(flow: http.HTTPFlow) -> None:
    # Check if the response contains HTML content

    if "image/jpeg" or "image/png" in flow.response.headers.get("content-type", ""):
        # Save the HTML content to a file with a unique name
        cur_time = str(time.time())
        filename = f"image_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.png"
        with open(filename, "wb") as f:
            f.write(flow.response.content)
        print(f"Saved Image content to {filename}")


    elif "text/html" in flow.response.headers.get("content-type", ""):
        # Save the HTML content to a file with a unique name
        cur_time = str(time.time())
        filename = f"html_{cur_time}_{flow.request.host}_path_{flow.request.path.replace('/', '_')}.html"
        with open(filename, "wb") as f:
        #with open(filename, "a") as f:
            f.write(flow.response.content)
        print(f"Saved HTML content to {filename}")

# Usage: mitmdump -s save_html.py
