import json

from cassandra.cluster import Cluster

from settings import CASSANDRA_HOST

cluster = Cluster([CASSANDRA_HOST])
session = cluster.connect()
session.execute(
    "CREATE KEYSPACE IF NOT EXISTS bitcoin WITH REPLICATION = { 'class' : 'SimpleStrategy', 'replication_factor' : 1 "
    "} AND durable_writes = true;")
session.execute("USE bitcoin;")
session.execute(
    "CREATE TABLE IF NOT EXISTS bitcoin.blocks_test (hash text, confirmations text, strippedsize text,"
    " size text, weight text, height text, version text, version_hex text, merkleroot text, "
    "time text, mediantime text, nonce text, bits text, difficulty text, chainwork text, n_tx text,"
    "previousblockhash text, nextblockhash text, data text, PRIMARY KEY (hash, height)) WITH CLUSTERING"
    " ORDER BY (height DESC);")
session.execute(
    "CREATE TABLE IF NOT EXISTS bitcoin.transactions_test (hash text, version text, size text, vsize text, "
    "weight text, locktime text, vin text, vout text, block_height text, PRIMARY KEY (hash, block_height))"
    " WITH CLUSTERING ORDER BY (block_height DESC);")

session.execute(
    "CREATE CUSTOM INDEX  IF NOT EXISTS vout_details ON bitcoin.transactions (vout) USING "
    "'org.apache.cassandra.index.sasi.SASIIndex' WITH OPTIONS = { 'mode': 'CONTAINS', 'analyzer_class': "
    "'org.apache.cassandra.index.sasi.analyzer.NonTokenizingAnalyzer', 'case_sensitive': 'false'};")


def write_to_cassandra(block):
    tries = 0
    done = False
    while tries < 3 and not done:
        tries += 1
        try:
            session.execute(
                """
        INSERT INTO bitcoin.blocks_test (hash, confirmations, strippedsize, size, weight, height, version, version_hex, merkleroot, time, mediantime, nonce, bits, difficulty, chainwork, n_tx, previousblockhash, nextblockhash, data)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s)
        """,
                (str(block['hash']), str(block['confirmations']), str(block['strippedsize']), str(block['size']),
                 str(block['weight']), str(block['height']), str(block['version']), str(block['versionHex']),
                 str(block['merkleroot']), str(block['time']), str(block['mediantime']), str(block['nonce']),
                 str(block['bits']), str(block['difficulty']), str(block['chainwork']), str(block['nTx']),
                 str(block['previousblockhash']), str(block['nextblockhash']),
                 str(json.dumps(block))))

            for tx in block['tx']:
                session.execute(
                    """
            INSERT INTO bitcoin.transactions_test (hash, version, size, vsize, weight, locktime, vin, vout, block_height)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """,
                    (str(tx['hash']), str(tx['version']), str(tx['size']), str(tx['vsize']), str(tx['weight']),
                     str(tx['locktime']), str(json.dumps(tx['vin']).encode('utf-8')),
                     str(json.dumps(tx['vout']).encode('utf-8')), str(block['height'])))
            done = True
        except Exception as e:
            print(e)

    return done
