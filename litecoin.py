import json
import requests
import logging

from kafka import store_in_big_data
from settings import LTC_BLOCK_TOPIC, LTC_HOST, LTC_PORT

logger = logging.getLogger("default")

# not defined in ltc
def get_block_hash(height):
    response = requests.get("http://{}:{}/rest/blockhashbyheight/{}.json".format(LTC_HOST, LTC_PORT, height))
    
    if response.status_code != 200:

        return
    
    return json.loads(response.text)['blockhash']


def get_block(block_hash):
    response = requests.get("http://{}:{}/rest/block/{}.json".format(LTC_HOST, LTC_PORT, block_hash))
    
    if response.status_code != 200:
        return 
    
    return json.loads(response.text)


def ltc():
    last_height = 0
    try:
        with open('checkpoints/ltc', 'r') as file:
            last_height = int(file.read().strip())
    except:
        pass

    while True:
        block_hash = get_block_hash(last_height)
        if block_hash:
            logger.info('storing block {}.'.format(block_hash))
            if store_in_big_data(LTC_BLOCK_TOPIC, get_block(block_hash)):
                last_height += 1
                with open('checkpoints/ltc', 'w') as file:
                    file.write(str(last_height))
            
        

if __name__ == "__main__":
    ltc()