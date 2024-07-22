#import mitmproxy_wireguard
import asyncio
import logging
import time
import configparser
import subprocess
from pathlib import Path
import json
import sys # version info

logging.Formatter.convert = time.gmtime
logger = logging.getLogger()

async def main():
    # import configuration files information
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_pubkey = config['CLIENT']['pub_key']
    email = config['CLIENT']['email']
    server_privkey = config['SERVER']['priv_key']
    server_pubkey = config['SERVER']['pub_key']
    wg_port = config['SERVER']['wg_port']

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


    logger.info(f"starting server with wireguard keys at {conf_file_path}")
    #subprocess.run(["mitmdump", "-s", "modify_response.py", "--mode", f"wireguard:{conf_file_path}@{wg_port}", "--certs", "*=cert.pem"]) # , stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(["mitmdump", "-s", "modify_response.py", "--mode", f"wireguard:{conf_file_path}@{wg_port}", "--set", "confdir=/.mitmproxy/"]) # , stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


    ########################
    logger.info("waiting on server to close")

if __name__ == '__main__':
    asyncio.run(main())

