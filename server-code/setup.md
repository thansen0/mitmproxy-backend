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
