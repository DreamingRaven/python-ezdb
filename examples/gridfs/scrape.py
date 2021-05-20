#!/usr/bin/env python3

# @Author: GeorgeRaven <archer>
# @Date:   2021-04-21T00:25:06+01:00
# @Last modified by:   archer
# @Last modified time: 2021-04-21T17:09:36+01:00
# @License: please see LICENSE file in project root

import os
import sys
import time
import numpy as np
import logging as logger
import getpass
import unittest
import io
from ezdb.mongo import Mongo
import configargparse as argparse
from tqdm import tqdm
import multiprocessing as mp


def arg_handler(argv, description: str = None):
    """Quick argument handler just to make everything easier to work with."""
    description = description if description is not None else "timelapse cam"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--db-ip",
                        type=str,
                        default="127.0.0.1",
                        env_var="DB_IP",
                        help="IP or hostname where db is accessible.")
    parser.add_argument("-p", "--db-port",
                        type=int,
                        default=27017,
                        env_var="DB_PORT",
                        help="Port where db is accessible.")
    parser.add_argument("-n", "--db-user-name",
                        type=str,
                        env_var="DB_USER_NAME",
                        help="Database username to use.")
    parser.add_argument("-P", "--db-password",
                        type=str,
                        env_var="DB_USER_PASSWORD",
                        help="Database user password for authentication.")
    parser.add_argument("--db-password-prompt",
                        type=bool,
                        default=False,
                        env_var="DB_USER_PASSWORD",
                        help="DB authentication using cli prompt.")
    parser.add_argument("-T", "--db-tls",
                        type=bool,
                        default=True,
                        env_var="DB_TLS",
                        help="Is databse TLS enabled.")
    parser.add_argument("-c", "--db-tls-ca-file",
                        type=str,
                        env_var="DB_TLS_CA_FILE",
                        default="lcas-mongo-CA.cert",
                        help="Certificate authority file to use if any.")
    parser.add_argument("-N", "--db-name",
                        type=str,
                        default="test",
                        env_var="DB_NAME",
                        help="Database to post data to.")
    parser.add_argument("-a", "--db-authentication-database",
                        type=str,
                        default="admin",
                        env_var="DB_AUTHENTICATION_DATABASE",
                        help="Database to authenticate to.")
    parser.add_argument("-C", "--db-collection-name",
                        type=str,
                        default="2021_riseholme_stationary_timelapse",
                        env_var="DB_COLLECTION_NAME",
                        help="Database collection to dump data to.")
    parser.add_argument("-v", "--debug", "--verbose",
                        action="store_true",
                        help="Debug/ verbose logging.")

    args = vars(parser.parse_args(argv))
    # spinning up logger
    logger.basicConfig(  # filename="{}.log".format(__file__),
        level=logger.DEBUG if args["debug"] is True else logger.INFO,
        format="%(asctime)s %(levelname)s:%(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S")
    args["pylog"] = logger.debug
    logger.debug("initial args: {}".format(args))
    # create password prompt if user has name but no pass or if specified to
    if (args["db_password_prompt"]) or \
            (args["db_password"] is None and args["db_user_name"] is not None):
        args["db_password"] = getpass.getpass()
    del args["db_password_prompt"]
    return args


class scrape_gridfs_db(unittest.TestCase):

    def setUp(self):
        """Connect to db and set up timer."""
        self.args = global_args
        self.startTime = time.time()

    def tearDown(self):
        """Consume time and display."""
        t = time.time() - self.startTime
        logger.info("{}: GridFS docs in {}".format(
            self.id(), t))

    def single_gridfs_data_stream(self, graphical=None):
        """Dump data to database sequentially."""
        db = Mongo(self.args)
        db.connect()
        cursor = db.getCursor(
            db_collection_name=self.args["db_collection_name"]+".files")
        for batch in tqdm(db.getFiles(db_data_cursor=cursor)):
            for grid in batch:
                print(grid["_id"])
                b = grid["gridout"].read()
                data = io.BytesIO(b)

                try:
                    filename = "{}_{}.jpeg".format(
                        grid["metadata"]["datetime"].strftime(
                            "%Y-%m-%dT%H:%M:%S"),
                        grid["_id"])
                except KeyError:
                    filename = "{}.jpeg".format(grid["_id"])

                if(os.path.isfile(filename) is not True):
                    print(filename)
                    with open(
                        filename,
                            "wb") as f:
                        f.write(data.getbuffer())
                else:
                    print(filename, "*")

    def test_single_stream_graphical(self):
        """Single process data stream."""
        self.single_gridfs_data_stream(graphical=True)


if __name__ == "__main__":
    # note setting this in global context for use in unittests
    global_args = arg_handler(sys.argv[1:],
                              description="Scrape a given collections GridFS.")
    # delete our cli args so unittest does not have a fit
    # we really shouldnt sideload args like this but its just a quick script
    del sys.argv[1:]
    # now call unittests to check everything through
    unittest.main()
