.. _section_mongo:

Mongo
=====

Nemesyst MongoDB abstraction/ Handler.
This handler helps abstract some pymongo functionality to make it easier for us to use a MongoDB database for our deep learning purposes.

Example usage
+++++++++++++

This unit test also briefly shows how to use gridfs by dumping tuple items in the form (dict(), object), where the dict will become the files metadata and the object is some form of the data that can be sequentialized into the database.

.. warning::

  Mongo uses subprocess.Popen in init, start, and stop, since these threads would otherwise lock up nemesyst, with time.sleep() to wait for the database to startup, and shutdown. Depending on the size of your database it may be necessary to extend the length of time time.sleep() as larger databases will take longer to startup and shutdown.

API
+++

.. autoclass:: ezdb.Mongo
  :members: