# MITM Proxy Setup

### Proxy Server

Run mitmproxy, and then run this line to open a new browser:

```
chromium --proxy-server="http://localhost:8080"
```

Everything falls into place and it works. The issue is the browser now prevents me from proceeding, which is annoying. Just turned off secure DNS so hopefully that fixes it.

The .pem file must be added where it says, you can't put it in an extra folder, unfortunately.

### mitmdump

```
./mitmdump -w writedata.txt
./mitmdump -s save_html.py
```

### TLS passthrough

This will allow all TLS through, while inspecting SSL and http

https://github.com/mitmproxy/mitmproxy/blob/main/examples/contrib/tls_passthrough.py

### Ignore hosts

This is a way to ignore hosts through the command line, although I can't find a way to do ir repeately in code

```
mitmdump --ignore-hosts reddit.com
```

# Machine Learning Models

### nsfw-detector 1.1.1

This one can be imported easily from pip, claims to be easy to use

https://pypi.org/project/nsfw-detector/

### nsfw-image-urls

Collection of urls to images of nsfw images. Could train on these if I want.

https://github.com/d00ML0rDz/nsfw-image-urls
