import mitmproxy_wireguard
import asyncio
import logging
import time
import os
import configparser
import subprocess
import textwrap
from modify_response import ModifyResponse

from mitmproxy.options import Options
#from mitmproxy.proxy.config import ProxyConfig
from mitmproxy.tools.dump import DumpMaster
#from mitmproxy.tools.main import mitmdump

logging.Formatter.convert = time.gmtime
logger = logging.getLogger()

public_ip_addr = "45.76.232.143" # ip you would ping to reach host server

async def main():
    global master
    # import configuration files information
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_pubkey = config['CLIENT']['pub_key']
    email = config['CLIENT']['email']
    server_privkey = config['SERVER']['priv_key']
    server_pubkey = config['SERVER']['pub_key']

    print(gen_client_conf(client_pubkey, server_privkey))
    wg_server = await mitmproxy_wireguard.start_server(
        "0.0.0.0",
        51820,
        server_privkey,
        [client_pubkey],
        handle_connection,
        receive_datagram,
    )

    options = Options(listen_host="0.0.0.0")
    master = DumpMaster(options, with_termlog=True, with_dumper=True)
    #options.block_global = False
    #master.addons.add(ModifyResponse()) # may have to remove addon in class??
    #master.addons.add() # may have to remove addon in class??
    master.server = wg_server


    try:
        print("starting server")
        # starting server
        await master.run()
    except:
        print("bad news bears")
        print(master)
        os._exit(1)

    ########################
#    wg0conf_path = "/wg0.conf"
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

    #print("starting server")
    #subprocess.run(["mitmdump", "-s", "modify_response.py", "--mode", "wireguard", "--certs", "/etc/keys/cert.pem"], shell=True, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    ########################
    def stop(*_):
        master.server.close()


    # Below also runs, unsure which is better
    #print("waiting on server to close")
    #await master.server.wait_closed()


def gen_client_conf(client_priv_key, server_pub_key):
    client_conf = textwrap.dedent(
        f"""
            [Interface]
            PrivateKey = {client_priv_key}
            Address = 10.0.0.1/32

            [Peer]
            PublicKey = {server_pub_key}
            AllowedIPs = 10.0.0.0/24
            Endpoint = {public_ip_addr}:51820
        """)


async def handle_connection(rw: mitmproxy_wireguard.TcpStream):
    print(rw)
    while True:
        data = await rw.read(65535) # 4096

        # check if the connection was closed
        if len(data) == 0:
            break

        try:
            rw.write(data)
        except:
            print("write failed")

        await rw.drain()

    rw.close()

def receive_datagram(data, src_addr, dst_addr):
#    print("data", data)
#    print("src",src_addr)
#    print("dst ",dst_addr)
    master.server.send_datagram(data.upper(), dst_addr, src_addr)

if __name__ == '__main__':
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(main())
    asyncio.run(main(), debug=True)
