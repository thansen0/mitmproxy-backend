#import mitmproxy_wireguard
import asyncio
import logging
import time
import configparser
import subprocess
from pathlib import Path
import json

logging.Formatter.convert = time.gmtime
logger = logging.getLogger()

public_ip_addr = "45.76.232.143" # ip you would ping to reach host server

async def main():
    # import configuration files information
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_pubkey = config['CLIENT']['pub_key']
    email = config['CLIENT']['email']
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
    # construct wireguard.conf key file
    conf_path = Path("wireguard.conf")
    conf_path.write_text(
        json.dumps(
            {
                "server_key": server_privkey,
                "client_key": client_pubkey,
            },
            indent = 4,
        )
    )

    conf_file_path = str(conf_path.absolute())



#    wg0conf_path = "wg0.conf"
#
#    conf_file_contents = f"""
#[Interface]
#Address = 10.0.0.1/32
#SaveConfig = true
#PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -t nat -A POSTROUTING -o enp1s0 -j MASQUERADE; iptables -t nat -A PREROUTING -i wg0 -p tcp -m tcp --dport 80 -j REDIRECT --to-port 8080; iptables -t nat -A PREROUTING -i wg0 -p tcp -m tcp --dport 443 -j REDIRECT --to-port 8080
#PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -t nat -D POSTROUTING -o enp1s0 -j MASQUERADE; iptables -t nat -D PREROUTING -i wg0 -p tcp -m tcp --dport 80 -j REDIRECT --to-port 8080; iptables -t nat -D PREROUTING -i wg0 -p tcp -m tcp --dport 443 -j REDIRECT --to-port 8080
#ListenPort = 51820
#PrivateKey = {server_privkey}
#
#[Peer]
#PublicKey = {client_pubkey}
#AllowedIPs = 10.0.0.2/24
#    """

    # create wgo.conf file
#    with open(wg0conf_path, "w") as conf_file:
#        conf_file.write(conf_file_contents)

    logger.info(f"starting server with wireguard keys at {conf_file_path}")
    subprocess.run(["mitmdump", "-s", "modify_response.py", "--mode", f"wireguard:{conf_file_path}@51820"]) # , stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    #subprocess.run(["mitmdump", "-s", "modify_response.py", "--mode", "wireguard", "--certs", "/etc/keys/cert.pem"], shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    ########################
    logger.info("waiting on server to close")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
