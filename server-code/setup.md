# MITM Docker Setup

## Using wireguard with mitmproxy

It turns out this is quite easy. From the command line it's just

```
mitmdump -s modify_response.py --mode wireguard
```

But it can also be done from a python file, which is how I'll have to do it.


## Dockerfile setup

We must build and then start the docker container

```
docker build -t mitmproxy .
docker run -p 8080:8080 mitmproxy
```

I used to do `docker run -it mitmproxy` for interactive tty terminal. We can also pass in certificates using the command

```
docker run -p 8080:8080 mitmproxy -v /path/to/cert.pem:/cert.pem
```

## Testing 

Testing can be done with the interactive terminal, so changing CMD to '/bin/bash' and then start it with 

```
docker run -p 8080:8080 -it mitmproxy
```

If I built a container and then stopped it, I can re enter it using exec

```
docker exec -it container_name /bin/bash
```

On the server wireguard usually runs on 51280 and you have to pass in the config.ini for terminal_run_wireguard.py to work, so you'll want to enable that port as well. We must specifically use /udp, otherwise it only allows tcp

```
docker run -p 51820:51820/udp --network=bridge -v /home/mitm/Code/mitmproxy/server-code/user_configs/username/0/config.ini:/config.ini -it mitmproxy

docker run --network=host -v /home/mitm/Code/mitmproxy/server-code/user_configs/fake/77/config.ini:/config.ini -it mitmproxy
```

A great line to test if I'm seeing data over a port is 

```
sudo tcpdump -i any -nn port 51820
```

### mitmproxy wireguard

We can set custom keys and port with the [command line option](https://docs.mitmproxy.org/stable/concepts-modes/#wireguard-transparent-proxy) as well

```
mitmdump -s modify_response.py --mode wireguard:~/Code/mitmproxy/server-code/wireguard.conf@51820
```

Where `wireguard.conf` is the private key for both the client and server

```
{
    "server_key": "server_priv_key"
    "client_key": "client_priv_key"
}
```

# Production

When running production you should be able to run `ClientConnectionServicer.py` and it will do everything else for you. Since this randomly chooses ports, we must allow ports through ufw. I did `sudo ufw disable` to turn off the firewall. This may want to be revised in the future but for now I think it's fine.

```
python ClientConnectionServicer.py
```

You also must create the certificate files, specifically two: public key (cert.crt), and public private combo (cert.pem)

```
openssl genrsa -out cert.key 2048
openssl req -new -x509 -key cert.key -out cert.crt
cat cert.key cert.crt > cert.pem
```

or using the `openssl.conf` file, we can build it using

```
openssl genrsa -out cert.key 2048
openssl req -new -x509 -key cert.key -out cert.crt -days 365 -config openssl.cnf
cat cert.key cert.crt > cert.pem

openssl x509 -in cert.crt -text -noout # for verification only
```

## Resources used

Each container takes about a half gig of ram, and a simple website with images can take 10-15% of each core on my two core regular cloud compute module (2GB RAM). A text website consumes basically no processing power. Getting a GPU powered box should be a high priority for production.

Starting a docker container brings a single core up to 100% for a second or two. Also we need to be sure we're deleting the image in code at some point because they take up a lot of storage space.

When loading `mobilenet_v2_140_224` it appears to use ~300 MB of VRAM. This may go up when I try predicting things, but overall it doesn't seem too high, likely due to the small model size.
