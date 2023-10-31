import mitmproxy_wireguard
import asyncio
import logging
import time
import configparser
#import textwrap3 as textwrap

logging.Formatter.convert = time.gmtime
logger = logging.getLogger()

public_ip_addr = "45.76.232.143"

async def main():
    def receive_datagram(data, src_addr, dst_addr):
        #logger.debug(f"Received datagram: {data=} {src_addr=} {dst_addr=}")
        server.send_datagram(data.upper(), dst_addr, src_addr)
        #logger.debug("Echoed datagram.")

    # import configuration files information
    config = configparser.ConfigParser()
    config.read('config.ini')
    client_pubkey = config['CLIENT']['pub_key']
    username = config['CLIENT']['username']
    server_privkey = config['SERVER']['priv_key']
    server_pubkey = config['SERVER']['pub_key']

    print("starting server")
    wg_server = await mitmproxy_wireguard.start_server(
        "0.0.0.0",
        51820,
        server_privkey,
        [client_pubkey],
        handle_connection,
        receive_datagram,
    )


#    client_conf = gen_client_conf(client_privkey, server_pubkey)
#    print(client_conf)

    def stop(*_):
        logger.info("STOPPING SERVER!!!! stop(*_) FUNCTION CALLED\n\n\n")
        print("STOPPING SERVER!!!! stop(*_) FUNCTION CALLED\n\n\n")
        wg_server.close()
        # TODO ultimately close whole docker container

    print("waiting on server to close")
    await wg_server.wait_closed()


async def handle_connection(rw: mitmproxy_wireguard.TcpStream):
    logger.debug(f"connection task {rw=}")
    logger.debug(f"{rw.get_extra_info('peername')=}")

    for _ in range(2):
        logger.debug("reading...")
        try:
            data = await rw.read(4096)
        except Exception as exc:
            logger.debug(f"read {exc=}")
            data = b""
        logger.debug(f"read complete. writing... {len(data)=} {data[:10]=} ")

        try:
            rw.write(data.upper())
        except Exception as exc:
            logger.debug(f"write {exc=}")
            logger.debug("write complete. draining...")
            
        try:
            await rw.drain()
        except Exception as exc:
            logger.debug(f"drain {exc=}")
        logger.debug("drained.")

    logger.debug("closing...")
    try:
        rw.close()
    except Exception as exc:
        logger.debug(f"close {exc=}")
    logger.debug("closed.")


#def gen_client_conf(client_priv_key, server_pub_key):
#    client_conf = textwrap.dedent(
#        f"""
#            [Interface]
#            PrivateKey = {client_priv_key}
#            Address = 10.0.0.1/32
#
#            [Peer]
#            PublicKey = {server_pub_key}
#            AllowedIPs = 10.0.0.0/24
#            Endpoint = {public_ip_addr}:51820
#        """)

    return client_conf

if __name__ == "__main__":
    asyncio.run(main())
    
