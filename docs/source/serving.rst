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

.. _letsencrypt: https://www.letsencrypt.org/
.. |letsencrypt| replace:: LetsEncrypt

.. _tls: https://docs.mongodb.com/manual/core/security-transport-encryption/
.. |tls| replace:: TLS/SSL

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

.. _page_serving:

Serving with |mongodb|_
=======================

|mongodb|_ is an object based database system. Python-ezdb provides a nice higher level interface "|section_mongo|" by using |pymongo|_ and os commands to make managing |mongodb|_ more streamlined and less reliant on direct connection management to |mongodb|_.

Creating a basic database
+++++++++++++++++++++++++

Disambiguation: we define a basic database as a standalone |mongodb|_ instance with one universal administrator and one read/write user with password authentication.

While it is possible it is highly discouraged to use Nemesyst to create the users you require as this is quite complicated to manage and may lead to more problems than its worth compared to simply creating a database and adding a user manually using something like the following:

.. _manual_mongodb:

Manual creation of |mongodb|_
-----------------------------

:|files-only| creation of database example\::

  .. parsed-literal::

      mongod --config ./examples/configs/basic_mongo_config.yaml

This will create a database with all the |mongodb|_ defaults as it is an empty |yaml|_ file.
If you would instead want a more complex setup please take a look at ``examples/configs/authenticated_replicaset.yaml`` instead, but you will need to generate certificates and keys for this so it is probably a poor place to start but will be what you will want to use in production as a bare minimum security.

|docker-compose|_ creation of |mongodb|_
----------------------------------------

:|docker-compose|_, |files-only| creation of database example\::

  .. parsed-literal::

      docker-compose up

This similar to the :ref:`manual_mongodb` creation uses a simple config file to launch the database. This can be changed in ``docker-compose.yaml``.
At this point you will need to connect to the running |mongodb|_ instance (see: :ref:`connecting_mongodb`) to create your main administrator user, with "userAdminAnyDatabase" role.
After this you can use the following to close the |docker|_ container with the database:

:|docker-compose|_, |files-only|, closing |docker-compose|_ database example\::

  .. parsed-literal::

      docker-compose down

.. note::
  Don't worry we set our docker-compose.yaml to save its files in ``/containers/mongodb`` so they are persistent between runs of docker-compose. If you need to delete the |mongodb|_ database that is where you can find them.

.. _connecting_mongodb:

Connecting to a running database
--------------------------------

To be able to fine tune, create users, update etc it will be necessary to connect to |mongodb|_ in one form or another. Nemesyst can help you log in or you can do it manually.

 .. note::
   If there is no `userAdmin or userAdminAnyDatabase <https://docs.mongodb.com/manual/reference/built-in-roles/#userAdmin>`_ then unless expressly configured there will be a localhost exception which will allow you to log in and create this user. If this user exists the localhost exception will close. Please ensure you configure this user as they can grant any role or rights to anyone and would be a major security concern along with making it very difficult to admin your database.

Mongo
*****

To connect to an non-sharded database with autnentication but no |tls|_:

:|bash shell|_ example\::

  .. parsed-literal::

      mongo |hostname|:|port| -u |username| --authenticationDatabase |dbname|

To connect to a slightly more complicated scenario with authentication, TLS, and sharding enabled:

:|bash shell|_ example\::

  .. parsed-literal::

      mongo |hostname|:|port| -u |username| --authenticationDatabase |dbname| --tls --tlsCAFile |cafile| --tlsCertificateKeyFile |certkeyfile|

Creating database users
-----------------------

You will absolutely need a user with at least "userAdminAnyDatabase" role.
Connect to the running database see :ref:`connecting_mongodb`.

:|mongo shell|_ create a new role-less user\::

  .. parsed-literal::

    db.createUser({user: "|username|", pwd: passwordPrompt(), roles: []})

:|mongo shell|_ grant role to existing user example\::

  .. parsed-literal::

    db.grantRolesToUser(
    "|username|",
    [
      { role: "|useradminanydb|", db: "|admin|" }
    ])

:|mongo shell|_ create user and grant |useradminanydb| in one\::

  .. parsed-literal::

    db.createUser({user: "|username|", pwd: passwordPrompt(), roles: [{role:"|useradminanydb|", db: "|admin|"}]})

.. note::
  Since this user belongs to |admin| in the previous examples that means the authenticationDatabase is |admin| when authenticating as this user as per the instructions in ":ref:`connecting_mongodb`".

From basic database to replica sets
+++++++++++++++++++++++++++++++++++

This section will outline how to take a currently standard database and turn it into a replica set

|mongodb| config file setup for replica sets
--------------------------------------------

:|files-only| example ``./examples/mongod.d/replica.yaml``\::

  .. literalinclude:: ../../examples/mongod.d/replica.yaml

Checking the current status of the replica sets
-----------------------------------------------

The replica sets should not be initialized which we can check.

:|mongo shell|_ Check the current status of replica sets\::

  Command:

  .. parsed-literal::

    rs.status()

  Out:

  .. parsed-literal::

    {
    	"operationTime" : Timestamp(0, 0),
    	"ok" : 0,
    	"errmsg" : "no replset config has been received",
    	"code" : 94,
    	"codeName" : "NotYetInitialized",
    	"$clusterTime" : {
    		"clusterTime" : Timestamp(0, 0),
    		"signature" : {
    			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
    			"keyId" : NumberLong(0)
    		}
    	}
    }

There should be no config present also, which we can also check.

:|mongo shell|_ Check the current status of replica set config\::

  Command:

  .. parsed-literal::

    rs.conf()

  Out:

  .. parsed-literal::

    2020-03-12T13:43:46.998+0000 E  QUERY    [js] uncaught exception: Error: Could not retrieve replica set config: {
    	"operationTime" : Timestamp(0, 0),
    	"ok" : 0,
    	"errmsg" : "no replset config has been received",
    	"code" : 94,
    	"codeName" : "NotYetInitialized",
    	"$clusterTime" : {
    		"clusterTime" : Timestamp(0, 0),
    		"signature" : {
    			"hash" : BinData(0,"AAAAAAAAAAAAAAAAAAAAAAAAAAA="),
    			"keyId" : NumberLong(0)
    		}
    	}
    } :
    rs.conf@src/mongo/shell/utils.js:1531:11
    @(shell):1:1

If the config does not yet exist like above, or is not initialized we should initialize it.

Initializing and populating the replica set config
--------------------------------------------------

:|mongo shell|_ Initialize the config\::

  Command:

  .. parsed-literal::

    rs.initiate()

Now the rs.conf should exist so we are free to add members to the replica set.

:|mongo shell|_ Add a member to the config\::

  Command:

  .. parsed-literal::

    rs.add({host: "|hostname|:|port|"})

From plaintext database to |tls|_
+++++++++++++++++++++++++++++++++

First it is necessary to generate a key and a certificate file for our use. For now these can be self signed but in future you may want to look at getting them signed by a certificate authority such as |letsencrypt|_.

Generating a certificate authority key, and then a self signed certificate
--------------------------------------------------------------------------

This example shows generating an encrypted RSA key. If you would instead prefer it to be plaintext remove ```-aes-256-cbc```.

:|bash shell|_ generate encrypted RSA certificate authority private key example\::

  .. parsed-literal::

      openssl genpkey -algorithm ``RSA`` ``-aes-256-cbc`` -pkeyopt rsa_keygen_bits:``4096`` -out ``ssl_key``

:|bash shell|_ generate x509 certificate file valid for 365 days example\::

  .. parsed-literal::

      openssl req -key ``ssl_key`` -x509 -new -days ``365`` -out ``signed_certificate``

.. note::
  It should be noted that MongoDB does hostname validation using this certificate file.
  The things we are aware of are the hostname must match, and in the case of replicas one thing like organization name must match between the communicating replicas if they use SSL/TLS.
  It should also be noted that Pymongo unlike mongo does not interpret between hostname and ip address the same way, an example can be found in |troubleshooting|.

This should now leave you with two files, an ``ssl_key`` and a ``signed_certificate``. We can now combine these two together to create a .pem file with both to provide to |mongodb|_.
This new file will is the certificate-key file.

:|bash shell|_ a |ckfile|_ file example\::

  .. parsed-literal::

      cat ``signed_certificate`` > |ckfile|_
      cat ``ssl_key`` >> |ckfile|_

Using our certificate and key as the server
-------------------------------------------

Almost all of the required changes take place in the mongodb config file/ how you call mongod itself.

:|files-only| ``mongod.conf``/ ``mongod.yaml`` example\::

  .. parsed-literal::

    net:
      bindIp: ``127.0.0.1``
      port: ``27017``
      tls:
        mode: requireTLS
        certificateKeyFile: |ckfile|_ # this should be a path to this file
        certificateKeyFilePassword: ``password``
        allowConnectionsWithoutCertificates: true

An example |tls|_ enabled replica set database config file can be seen below. This however requires a few additional files for authenticating the databases and certificates for SSL/TLS that you will need to generate.

:|files-only| example ``./examples/mongod.d/authenticated_replicaset.yaml``\::

  .. literalinclude:: ../../examples/mongod.d/authenticated_replicaset.yaml

Using our certificate and key as the client
-------------------------------------------

Self signed certificates are just as valid, and as good as any other certificate, with one exception; only machines we can install our certificate on will trust us, unless we disable this layer of trust entirely. Thus if our certificate is self signed then the certificate file in our case ``signed_certificate`` must be installed on each machine that we desire to trust our |mongodb|_ instance.

Troubleshooting
+++++++++++++++

Please see |troubleshooting|

Further reading
+++++++++++++++

|mongodb|_ core:

- `config file options <https://docs.mongodb.com/manual/reference/configuration-options/>`_
- `user management <https://docs.mongodb.com/manual/tutorial/manage-users-and-roles/#manage-users-and-roles/>`_

..
  https://docs.mongodb.com/manual/reference/glossary/#term-init-script

|replica|_ sets:

- `rs.initiate <https://docs.mongodb.com/manual/reference/method/rs.initiate//>`_
- `add members <https://docs.mongodb.com/manual/tutorial/expand-replica-set//>`_

|tls|_:

- `arch wiki tls <https://wiki.archlinux.org/index.php/Transport_Layer_Security/>`_

..
  `link template </>`_
