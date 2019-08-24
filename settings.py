import os
from logging.config import dictConfig

dictConfig({
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        },
        "verbose": {
            "format": "%(levelname)3.3s %(asctime)22.22s %(process)7d [%(name)s:%(funcName)s] %(message)s"
        }
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler"
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler"
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": "debug.log",
            "formatter": "simple"
        }
    },
    "loggers": {
        "default": {
            "handlers": [
                "console",
            ],
            "level": "INFO"
        }
    }
})

conf = {'bootstrap.servers': os.environ.get('BOOSTRAP_SERVER'),
        'queue.buffering.max.ms': 400,
        'linger.ms': 400,
        'queue.buffering.max.messages': '1000000',
        'message.max.bytes': 1024 * 1024 * 60,
        'client.id': os.environ.get('CLIENT_ID'),
        }

BTC_BLOCK_TOPIC = 'bitcoin'
BTC_HOST = os.environ.get('BTC_HOST', '172.17.0.1')
BTC_PORT = os.environ.get('BTC_PORT', '8332')

LTC_BLOCK_TOPIC = 'litecoin'
LTC_HOST = os.environ.get('BTC_HOST', '172.17.0.1')
LTC_PORT = os.environ.get('BTC_PORT', '9332')

ETH_BLOCK_TOPIC = 'eth'
ETH_HOST = os.environ.get('ETC_HOST', '172.17.0.1')
ETH_PORT = os.environ.get('ETH_PORT', '8545')
