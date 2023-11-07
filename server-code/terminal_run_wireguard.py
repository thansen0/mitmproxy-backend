import mitmproxy_wireguard
import asyncio
import logging
import time
import configparser
import subprocess

logging.Formatter.convert = time.gmtime
logger = logging.getLogger()

public_ip_addr = "45.76.232.143" # ip you would ping to reach host server

async def main():
    # import configuration files information
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_pubkey = config['CLIENT']['pub_key']
    username = config['CLIENT']['username']
    server_privkey = config['SERVER']['priv_key']
    server_pubkey = config['SERVER']['pub_key']

    #wg_server = await mitmproxy_wireguard.start_server(
    #    "0.0.0.0",
    #    51820,
    #    server_privkey,
    #    [client_pubkey],
    #    handle_connection,
    #    receive_datagram,
    #)

    ########################
    wg0conf_path = "/wg0.conf"
    client_ip_addr = "71.87.47.163" # maybe 0.0.0.0?

    conf_file_contents = f"
[Interface]
Address = 10.0.0.1/24
SaveConfig = true
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE; iptables -t nat -A PREROUTING -i wg0 -p tcp -m tcp --dport 80 -j REDIRECT --to-port 8080; iptables -t nat -A PREROUTING -i wg0 -p tcp -m tcp --dport 443 -j REDIRECT --to-port 8080
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp1s0 -j MASQUERADE; iptables -t nat -D PREROUTING -i wg0 -p tcp -m tcp --dport 80 -j REDIRECT --to-port 8080; iptables -t nat -D PREROUTING -i wg0 -p tcp -m tcp --dport 443 -j REDIRECT --to-port 8080
ListenPort = 51820
PrivateKey = {server_privkey}

[Peer]
PublicKey = {client_pubkey}
AllowedIPs = 10.0.0.2/32
Endpoint = {client_ip_addr}:51820
    "

    # create wgo.conf file
    with open(wg0conf_path, "w") as conf_file:
        conf_file.write(conf_file_contents)

    print("starting server")
    subprocess.run(["mitmdump", "-s", "modify_response.py", "--mode", "wireguard", "--certs", "cert.pem" ])


    ########################




#    client_conf = gen_client_conf(client_privkey, server_pubkey)
#    print(client_conf)

    print("waiting on server to close")

