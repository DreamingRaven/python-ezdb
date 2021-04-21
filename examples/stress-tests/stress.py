#!/usr/bin/env python3

import sys
import time
import numpy as np
import logging as logger
import getpass
import unittest
from ezdb.mongo import Mongo
import configargparse as argparse


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
                        default="lcas-mongo.CA.cert",
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
                        default="stress-test",
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
    # create password prompt if user has name but no pass or if specified to
    if (args["db_password_prompt"]) or \
            (args["db_password"] is None and args["db_user_name"] is not None):
        args["db_password"] = getpass.getpass()
    del args["db_password_prompt"]
    return args


class stress_db(unittest.TestCase):

    def setUp(self):
        """Connect to db and set up timer."""
        self.db = Mongo(args)
        self.db.connect()
        self.startTime = time.time()
        self.data = [
            # comment or uncomment what you most closeley matches your use
            # you can uncomment multiple if you have multi-varying inputs

            # standard full HD image
            np.random.rand(1920, 1080, 3),

            # depth map
            np.random.rand(848, 480, 1),

            # aligned depth map
            np.random.rand(1920, 1080, 1),
        ]

    def tearDown(self):
        """Consume time and display."""
        t = time.time() - self.startTime
        print('%s: %.3f' % (self.id(), t))

    def test_stress_gridfs(self):
        """Stress test repeated large gridfs documents."""
        for data in self.data:
            pass


if __name__ == "__main__":
    # note setting this in global context for use in unittests
    args = arg_handler(sys.argv[1:],
                       description="Stress test a given database.")
