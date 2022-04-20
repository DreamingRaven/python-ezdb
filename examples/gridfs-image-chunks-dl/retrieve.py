# from nemesyst_core.mongo import Mongo
# pip3 install git+https://github.com/DreamingRaven/python-ezdb.git#branch=master
from ezdb.mongo import Mongo  # github.com/DreamingRavn/python-ezdb
from datetime import datetime, tzinfo, timezone
import io
import os
import glob

###############
# CONFIGURATION
###############

time_restricted_pipeline = [
    {
        '$sort': {
            'datetime': -1
        }
    }, {
        '$addFields': {
            'hour': {
                '$hour': '$datetime'
            }
        }
    },
    {
        '$match': {
            'hour': {
                '$gte': 5,
                '$lt': 20
            }
        }
    },
    {
        '$match': {
            'datetime': {
                '$gte': datetime(2020, 4, 29, 0, 0, 0, tzinfo=timezone.utc)
            }
        }
    }
]

# change this to be the collection of concern without any extension like .files or .chunks
top_level_collection_name = "2020_riseholme_stationary_timelapse"

db_config = {
    # populate the database credentials being moved TO on the REMOTE system
    # for possible options see:
    # https://python-ezdb.readthedocs.io/en/latest/mongo.html#ezdb.mongo.Mongo.connect
    "db_ip": "domain.com",  # whatever the dns or ip is of remote db
    "db_port": 80, # most mongodb instances use 27017 by default so check which port you desire
    "db_user_name": "user",  # whatever the username is
    "db_password": "********",  # the users password
    "db_authentication_database": "berry",  # the authenticated to coll
    "db_tls": True,  # secure communication with tls
    "db_tls_ca_file": "CA.cert",  # path to tls certificate
    "db_name": "berry",  # database to sync TO name
    "db_collection_name": str(top_level_collection_name) + ".files",  # unused as we set it explicitly in mapping
    "pylog": logging.debug,  # what logger to use
}

#######################
# JPEG DOWNLOAD FROM DB
#######################

db_connect_args = db_config
projection = [{'$project': {'_id': 1}}]

db = Mongo(db_connect_args)
db.connect()
db.getCursor(db_collection_name=db_connect_args["db_collection_name"],
             db_pipeline=db["db_pipeline"].extend(projection))
# db.debug()

every_id = []
# check verify if files exist already
for batch in db.getBatches():
    every_id.extend(
        list(map(lambda doc: str(doc["_id"]), batch))
    )

print(every_id)
file_names = [f for f in glob.glob("*.jpeg")]
print(file_names)

# get data that does not already exist from database
print(db_connect_args["db_pipeline"])
db.getCursor(db_collection_name=db_connect_args["db_collection_name"],
             db_pipeline=db_connect_args["db_pipeline"])
print("begin stream... (* files that exist in filesystem will be skipped)")
for batch in db.getFiles(db_collection_name=top_level_collection_name):
    for grid in batch:
        image = grid["gridout"].read()
        image = io.BytesIO(image)
        filename = "{}_{}.jpeg".format(grid["metadata"]["datetime"].strftime(
            "%Y-%m-%dT%H:%M:%S"),
            grid["_id"])
        if(os.path.isfile(filename) is not True):
            print(filename)
            with open(
                "{}_{}.jpeg".format(
                    grid["metadata"]["datetime"].strftime(
                        "%Y-%m-%dT%H:%M:%S"),
                    grid["_id"]),
                    "wb") as f:
                f.write(image.getbuffer())
        else:
            print(filename, "*")
