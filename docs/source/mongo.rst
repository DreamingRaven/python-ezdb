.. _section_mongo:

Mongo
=====

ezdb.mongo.Mongo
++++++++++++++++

Nemesyst MongoDB abstraction/ Handler.
This handler helps abstract some pymongo functionality to make it easier for us to use a MongoDB database for our deep learning purposes.

Example usage
+++++++++++++

This unit test also briefly shows how to use gridfs by dumping tuple items in the form (dict(), object), where the dict will become the files metadata and the object is some form of the data that can be sequentialized into the database.

.. warning::

  Mongo uses subprocess.Popen in init, start, and stop, since these threads would otherwise lock up ezdb.mongo.Mongo, with time.sleep() to wait for the database to startup, and shutdown. Depending on the size of your database it may be necessary to extend the length of time time.sleep() as larger databases will take longer to startup and shutdown.

Setting up a basic database, and initializing it with a user.

.. literalinclude:: ../../unit_test.py
    :pyobject: Mongo_tests.setUp

Connecting to and dumping data to a database using normal mongodb requests.

.. literalinclude:: ../../unit_test.py
    :pyobject: Mongo_tests.test_dump

Using Gridfs to dump larger files in chunks to database.

.. literalinclude:: ../../unit_test.py
    :pyobject: Mongo_tests.test_gridfs

Completely removing the database, this completely removes all your data.

.. literalinclude:: ../../unit_test.py
    :pyobject: Mongo_tests.tearDown

API
+++

.. autoclass:: ezdb.mongo.Mongo
  :members:
