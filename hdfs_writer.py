from json import dumps

from hdfs import InsecureClient
from settings import HDFS_PORT, HTFS_HOST

client = InsecureClient('http://{}:{}'.format(HTFS_HOST, HDFS_PORT), user='khame')

writer = client.write('bitcoin_test')


def write_to_hdfs(block):
    writer.write(dumps(block))
    return True