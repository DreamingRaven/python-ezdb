.. |files-only| replace:: :ref:`section_files-only`

.. _sklearn: https://scikit-learn.org/stable/index.html
.. |sklearn| replace:: scikit-learn

.. _mongodb: https://www.mongodb.com/
.. |mongodb| replace:: MongoDB

.. _yaml: https://yaml.org/
.. |yaml| replace:: yaml

.. _mongodb compass: https://www.mongodb.com/products/compass
.. |mongodb compass| replace:: MongoDB Compass

.. _replica: https://docs.mongodb.com/manual/replication/
.. |replica| replace:: Replica

.. _mongo shell: https://docs.mongodb.com/manual/mongo/
.. |mongo shell| replace:: Mongo shell

.. _bash shell: https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29
.. |bash shell| replace:: Bash shell

.. _docker: https://www.docker.com/
.. |docker| replace:: Docker

.. _docker-compose: https://docs.docker.com/compose/
.. |docker-compose| replace:: Docker-Compose

.. _pymongo: https://api.mongodb.com/python/current/
.. |pymongo| replace:: PyMongo

.. _ckfile: https://docs.mongodb.com/manual/tutorial/configure-ssl/#mongod-and-mongos-certificate-key-file
.. |ckfile| replace:: ``ckfile.pem``

.. |troubleshooting| replace:: :ref:`section_ts_mongodb`
.. |section_mongo| replace:: :ref:`section_mongo`

.. |hostname| replace:: ``hostname``
.. |port| replace:: ``port``
.. |username| replace:: ``username``
.. |dbname| replace:: ``database name``
.. |cafile| replace:: ``path to ca file``
.. |certkeyfile| replace:: ``path to cert key file``
.. |useradminanydb| replace:: ``userAdminAnyDatabase``
.. |admin| replace:: ``admin``

troubleshooting
===============

.. _section_ts_mongodb:

MongoDB/ Serving Issues
+++++++++++++++++++++++

:Error\: not master and slaveOk=false:

  This error means you have attempted to read from a replica set that is not the master. If you would like to read from SECONDARY-ies/ slaves (anything thats not the PRIMARY) you can:

  :|mongo shell|_\::

    .. parsed-literal::

        `rs.slaveOk() <https://docs.mongodb.com/manual/reference/method/rs.slaveOk/>`_

:pymongo.errors.OperationFailure\: Authentication failed:

  This error means likely means that your authentication credentials are incorrect, you will want to check the values you are passing to pymongo via Nemesyst to ensure they are what you are expecting. In particular pay special attention to Mongo().connect() as it is the life blood of all connections but since the driver is a lazy driver it wont fail until you attempt to use the connection.

:pymongo.errors.ServerSelectionTimeoutError\: 192.168.1.10\:27017\: [SSL\: CERTIFICATE_VERIFY_FAILED] certificate verify failed\: IP address mismatch, certificate is not valid for '192.168.1.10':

  This error is a implementation quirk of pymongo not converting between ip addresses and hostname strings implicitly even if the certificate stipulates the desired IP address correctly for other things such as the mongo client.
  My only recommendation is to either use hostnames even if that only be explicit in ``/etc/hosts`` or disabling TLS but both are bad options for anything more than testing.
