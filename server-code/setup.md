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

On the server wireguard usually runs on 51280 and you have to pass in the config.ini for terminal_run_wireguard.py to work, so you'll want to enable that port as well

```
docker run -p 51820:51820 -v /home/mitm/Code/mitmproxy/server-code/user_configs/username/0/config.ini:/config.ini -it mitmproxy
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

