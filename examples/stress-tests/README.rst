Database Stress Testing
=======================

Ths dir contains a helpful dockerised and parameterisable unittest script that you should add/ take away from to enable single threaded stress testing of a given MongoDB database.

To build the container (and copy in any files in this directory):

.. code-block:: bash

  docker build -t archer/stress -f Dockerfile .

To run this container interactively:

.. code-block:: bash

  docker run -it archer/stress

This should automatically post a help page to indicate what parameters you might want to add. To pass in parameters to the docker script simply add them to the end of the above:

.. code-block:: bash

  docker run -it archer/stress --db-port 27017 --db-user-name me --db-password-prompt True

If you need to give it a TLS certificate just drop it in this directory, rebuild the docker image, then the container with the --db-tls-ca-file option giving the files name.

If you require access to localhost or some local/ internal port then consider using host networking:

.. code-block:: bash

  docker run --network host -it archer/stress
