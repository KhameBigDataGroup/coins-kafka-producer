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
        "filename": "/logs/debug.log",
        "formatter": "simple"
      }
    },
    "loggers": {
      "root": {
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
        'client.id': os.environ.get('CLIENT_ID'),
        }

BTC_BLOCK_TOPIC = 'bitcoin'
BTC_HOST = '172.17.0.1'
BTC_PORT = '8332'
