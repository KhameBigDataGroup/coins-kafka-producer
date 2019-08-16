import json
import requests
import logging

from eth_rpc_client import Client

from kafka import store_in_big_data
from settings import ETH_BLOCK_TOPIC, ETH_HOST, ETH_PORT

logger = logging.getLogger(__file__)

client = Client(host=ETH_HOST, port=ETH_PORT)

def get_block_hash(height):
    response = requests.get("http://{}:{}/rest/blockhashbyheight/{}.json".format(BTC_HOST, BTC_PORT, height))

    client.get_block_by_number()
    if response.status_code != 200:
        return

    return json.loads(response.text)['blockhash']


def get_block(block_hash):
    response = requests.get("http://{}:{}/rest/block/{}.json".format(BTC_HOST, BTC_PORT, block_hash))

    if response.status_code != 200:
        return

    return json.loads(response.text)


def btc():
    last_height = 0
    try:
        with open('checkpoints/btc', 'r') as file:
            last_height = int(file.read().strip())
    except:
        pass

    while True:
        client.get_block_by_number(last_height)
        if block_hash:
            logger.info('storing block {}.'.format(block_hash))
            if store_in_big_data(ETH_BLOCK_TOPIC, ):
                last_height += 1
                with open('checkpoints/btc', 'w') as file:
                    file.write(str(last_height))


if __name__ == "__main__":
    btc()