#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2019-07-15
# @Email:  george raven community at pm dot me
# @Filename: ezdb.py
# @Last modified by:   archer
# @Last modified time: 2021-05-20T11:55:33+01:00
# @License: Please see LICENSE in project root

# from __future__ import print_function, absolute_import   # python 2-3 compat
import unittest


class Mongo_tests(unittest.TestCase):
    """Unit test class aggregating all tests for the Mongo class

    There will be imports within functions here, this is to create complete
    examples for generating docs with.
    """

    def setUp(self):
        """Predefined setUp function for preparing tests, in our case
        creating the database."""
        import os
        from ezdb.mongo import Mongo

        # the path and directory we want to use to store the database files
        db_path = "./unit_test_db"
        db = Mongo({"pylog": null_printer, "db_path": db_path,
                    "db_log_path": db_path})
        # initialise the database files and create a basic user
        db.init()
        # start the database with authenticaton
        db.start()

        # for tests only to check db directory is created
        self.assertTrue(os.path.isdir(db_path))

    def tearDown(self):
        """Predefined tearDown function for cleaning up after tests,
        in our case deleting any generated db files."""
        import os
        import shutil
        from ezdb.mongo import Mongo

        db_path = "./unit_test_db"
        db = Mongo({"pylog": null_printer, "db_path": db_path,
                    "db_log_path": db_path})
        db.stop()
        if(db_path is not None):
            shutil.rmtree(db_path)

        # for tests only to check db directory has been removed
        self.assertFalse(os.path.isdir(db_path))

    def test_dump(self):
        """Test/ example of dump and retrieve from a MongoDB database."""
        from ezdb.mongo import Mongo

        db = Mongo({"pylog": null_printer})
        self.assertIsInstance(db, Mongo)
        db.connect()
        db.dump(db_collection_name="test", data={"success": 1})
        cursor = db.getCursor(db_collection_name="test")
        for batch in db.getBatches(db_data_cursor=cursor):
            self.assertEqual(len(batch), 1)
            for doc in batch:
                self.assertEqual(doc["success"], 1)

    def test_donate(self):
        """Test/ example of donating data to another collection."""
        from ezdb.mongo import Mongo

        db = Mongo({"pylog": null_printer})
        self.assertIsInstance(db, Mongo)
        db.connect()

        # insert data in the donor collection
        db.dump(db_collection_name="donor", data={"success": 1})

        # donate data
        db.getCursor(db_collection_name="rec")
        db.donate(other=db, other_collection="rec", db_collection_name="donor")

        # check donated data is correct
        cursor = db.getCursor(db_collection_name="rec")
        for batch in db.getBatches(db_data_cursor=cursor):
            self.assertEqual(len(batch), 1)
            for doc in batch:
                self.assertEqual(doc["success"], 1)

    def test_gridfs(self):
        """Test/ example of gridfs dump and retrieve from MongoDB."""
        from ezdb.mongo import Mongo

        db = Mongo({"pylog": null_printer})
        self.assertIsInstance(db, Mongo)
        db.connect()
        db.dump(db_collection_name="test", data=({"success": 1}, b'success'))
        cursor = db.getCursor(db_collection_name="test.files")
        for batch in db.getFiles(db_data_cursor=cursor):
            for grid in batch:
                # check ids match
                self.assertEqual(grid["_id"], grid["metadata"]["_id"])
                # read file and check is equal to what we put in
                self.assertEqual(grid["gridout"].read(), b'success')

    def test_delete(self):
        """Test that we can delete items from db correctly by id."""
        from ezdb.mongo import Mongo

        db = Mongo({"pylog": null_printer})
        self.assertIsInstance(db, Mongo)
        db.connect()
        db.dump(db_collection_name="test", data={"success": 1})
        cursor = db.getCursor(db_collection_name="test")
        for batch in db.getBatches(db_data_cursor=cursor):
            self.assertEqual(len(batch), 1)
            for doc in batch:
                self.assertEqual(doc["success"], 1)
                db.deleteId(db_collection_name="test", id=doc["_id"])

        cursor = db.getCursor(db_collection_name="test")
        deleted_collection = list(db.getBatches(db_data_cursor=cursor))
        self.assertEqual(deleted_collection, [])

    def test_userAdd(self):
        from ezdb.mongo import Mongo

        db = Mongo({"pylog": null_printer})
        self.assertIsInstance(db, Mongo)
        db.connect()
        a = db.userAdd(username="test", password="test", roles=["readWrite"])
        b = db.userInfo(username="test")
        print("TEST USER ADD: {}, {}".format(a, b))


def null_printer(*text, log_min_level=None,
                 log_delimiter=None):
    # do absoluteley nothing, i.e dont print
    pass


if __name__ == "__main__":
    # run all the unit-tests
    unittest.main()
