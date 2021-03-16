#!/usr/bin/env python3

# @Author: GeorgeRaven <archer>
# @Date:   2020-07-20T15:30:09+01:00
# @Last modified by:   archer
# @Last modified time: 2021-03-16T10:15:10+00:00
# @License: please see LICENSE file in project root


from ezdb.mongo import Mongo
import logging
import numpy as np
import datetime
import time

# feel free to modify this to whatever you like even not using a file at all
logging.basicConfig(filename="./sync.log", level=logging.DEBUG,
                    format="%(asctime)s %(levelname)s:%(message)s",
                    datefmt="%Y-%m-%dT%H:%M:%S")

logging.info("Starting Sync")
print("\nStarting Sync {}".format(datetime.datetime.utcnow()))

lcas_config = {
    # populate the database credentials being moved TO on the REMOTE system
    # for possible options see:
    # https://python-ezdb.readthedocs.io/en/latest/mongo.html#ezdb.mongo.Mongo.connect
    "db_ip": "domain.com",  # whatever the dns or ip is of remote db
    "db_port": 80,
    "db_user_name": "user",  # whatever the username is
    "db_password": "********",  # the users password
    "db_authentication_database": "berry",  # the authenticated to coll
    "db_tls": True,  # secure communication with tls
    "db_tls_ca_file": "CA.cert",  # path to tls certificate
    "db_name": "berry",  # database to sync TO name
    "db_collection_name": "test",  # unused as we set it explicitly in mapping
    "pylog": logging.debug,  # what logger to use
}

local_config = {
    # populate the database credentials being moved FROM on the LOCAL system
    # for possible options see:
    # https://python-ezdb.readthedocs.io/en/latest/mongo.html#ezdb.mongo.Mongo.connect
    "db_ip": "127.0.0.1",  # where db is locally accessible
    "db_port": 65530,  # db local port
    "db_name": "local_store",  # db local name
    "db_authentication": None,  # whatever authentication you use see link abv
    "pylog": logging.debug,  # whatever logger you want
}

lcas = Mongo(lcas_config)
local_db = Mongo(local_config)

local_db.debug()
lcas.debug()

local_db.connect()
lcas.connect()

collection_mapping = {
    # A collection map, that lists which collection goes where.
    # source-collection -> destination-collection
    "source1": "destination1",
    "source2": "destination2",
}

logging.info("Collection mapping: {}".format(collection_mapping))

id_pipeline = [
    {
        '$project': {
            '_id': 1
        }
    }
]

# hold on before starting just in case, to prevent instant bombing of resources
time.sleep(10)

index = 0
for key in collection_mapping:
    logging.info("Donating collection: '{}'".format(key))
    local_db.getCursor(db_collection_name=key)
    ids = local_db.donate(other=lcas,
                          db_collection_name=key,
                          other_collection=collection_mapping[key],
                          )
    logging.info("Documents copied: {}".format(len(ids)))
    logging.info("Finished donating collection: '{}'".format(key))
    index = index + 1

# hold on for a few minutes after completing, to reduce strain
time.sleep(290)
