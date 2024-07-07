# Commands to start a new server

We start out on root, so we need to create a new user.

```
sudo adduser mitm # I'll have to set a password
sudo usermod -aG sudo mitm
su - mitm
```

Add ssh keys from my machine

```
# add to .ssh/config
ssh-copy-id vultr-vps-name
```

The back on the remote server, I have to add keys for github and clone the repo

```
ssh-keygen -t rsa -b 4096 -C "ADD EMAIL"
mkdir Code && cd Code
sudo apt install git tmux python3.11-venv
git clone git@github.com:thansen0/mitmproxy-backend.git
cd mitmproxy-backend
git clone git@github.com:thansen0/mitmproxy-pubkey.git
# change public_ip_addr in server-code/terminal_run_wireguard.py

sudo apt install docker docker-compse
# ADD TO /etc/sudoers: `%docker ALL=(ALL) NOPASSWD: /usr/bin/docker`
sudo usermod -a -G docker $USER
```

Create venv environment, and install pip packages for ImageClassifier

```
# in mitmproxy-backend
mkdir venv
python -m venv venv
pip install protobuf==3.20.* tensorflow==2.12.1 nsfw-detector mitmproxy_rs docker cryptography pillow
# pip install grpcio grpcio-tools # for compiling protobuf tools

wget https://github.com/GantMan/nsfw_model/releases/download/1.1.0/nsfw_mobilenet_v2_140_224.zip
unzip nsfw_mobilenet_v2_140_224.zip
```

Also need to build protos for gRPC

```
cd protos

sudo ufw allow 50059/tcp # maybe not needed? check whether tcp/udp/if at all req
sudo ufw allow 50059/udp
# for wireguard data, although this didn't fix the issue
sudo ufw allow 1024:65535/udp
sudo ufw allow 1024:65535/udp
```

I need to move the following files over from the old to new server:

```
wireguard.conf
cert.pem
```

I lastly need to be sure to make changes to these files:

 1. Change host IP address in ClientConnectionService.py
 2. Add real redis information to redis-config.ini
