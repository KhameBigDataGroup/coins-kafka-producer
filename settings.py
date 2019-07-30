import os

conf = {'bootstrap.servers': os.environ.get('BOOSTRAP_SERVER'),
        'queue.buffering.max.ms': 400,
        'linger.ms': 400,
        'queue.buffering.max.messages': '1000000',
        'client.id': os.environ.get('CLIENT_ID'),
        }

BTC_BLOCK_TOPIC = 'btc-block'
BTC_HOST = 'localhost'
BTC_PORT = '8332'
