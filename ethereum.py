import json
import requests
import logging

from eth_rpc_client import Client

from kafka import store_in_big_data
from settings import ETH_BLOCK_TOPIC, ETH_HOST, ETH_PORT

logger = logging.getLogger(__file__)

client = Client(host=ETH_HOST, port=ETH_PORT)


def get_block_by_number(number):
    json_response = json.loads(requests.post('http://{}:{}/'.format(ETH_HOST, ETH_PORT),
                                             json={"jsonrpc": "2.0", "method": "eth_getBlockByNumber",
                                                   "params": [hex(number), True],
                                                   "id": 1}).content.decode())
    if 'error' in json_response:
        return None
    return json_response['result']


def eth():
    last_height = 0
    try:
        with open('checkpoints/eth', 'r') as file:
            last_height = int(file.read().strip())
    except:
        pass

    while True:
        block = get_block_by_number(last_height)
        if block:
            logger.info('storing block {}.'.format(block['hash']))
            if store_in_big_data(ETH_BLOCK_TOPIC, block):
                last_height += 1
                with open('checkpoints/eth', 'w') as file:
                    file.write(str(last_height))


if __name__ == "__main__":
    eth()
