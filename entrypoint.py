import json

import websocket
from confluent_kafka import Producer
import logging

from kafka import store_in_big_data
from settings import BTC_TRANSACTION_TOPIC, BTC_BLOCK_TOPIC

logger = logging.getLogger(__name__)


class UnknownOPException(Exception):
    pass


def on_message(ws, message):
    try:
        data = json.loads(message)
        if data['op'] == 'utx':
            topic = BTC_TRANSACTION_TOPIC
        elif data['op'] == 'block':
            topic = BTC_BLOCK_TOPIC
        else:
            raise UnknownOPException(data['op'])
        store_in_big_data(topic, data)
    except Exception as e:
        print(e)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    ws.send('{"op":"unconfirmed_sub"}')
    ws.send('{"op":"blocks_sub"}')


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv/",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
