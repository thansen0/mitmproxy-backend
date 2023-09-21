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

This has to be installed in a specific order or else it will have conflicts.

```
pip install protobuf==3.20.*
# pip install tensorflow==2.12.1 # I don't think it's needed
pip install nsfw-detector

wget https://github.com/GantMan/nsfw_model/releases/download/1.1.0/nsfw_mobilenet_v2_140_224.zip
nsfw-predict --saved_model_path mobilenet_v2_140_224 --image_source fill.jpeg
```

### nsfw-image-urls

Collection of urls to images of nsfw images. Could train on these if I want.

https://github.com/d00ML0rDz/nsfw-image-urls

## Connecting to remote server

SSH into server, open up ports. Then run mitmdump with the command

```
mitmdump -s save_html.py --set block_global=false
```

where block global allows you to listen on public IP addresses (such as any user). Then on my machine I run

```
chromium --proxy-server="http://45.76.232.143:8080"
```

## ssh tunneling with password (password optional)

Initiate tunnel using -L command, * means all domains.

```
ssh -L 8080:*:8080 mitm-nogpu
...
mitmdump -s modify_response.py --proxyauth username:password
```

And then connect with a browser like it was a local server

```
chromium --proxy-server="http://localhost:8080"
```
