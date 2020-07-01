.. _page_installation:

.. _git: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
.. |git| replace:: git

.. _python:  https://www.python.org/
.. |python| replace:: python

.. _mongodb: https://www.mongodb.com/
.. |mongodb| replace:: MongoDB

.. _docker: https://www.docker.com/
.. |docker| replace:: Docker

.. _bash shell: https://en.wikipedia.org/wiki/Bash_%28Unix_shell%29
.. |bash shell| replace:: Bash shell

.. |dockerisation| replace:: :ref:`section_docker`

Installation
============

.. note::

    Certain distributions link ``python`` to ``python2`` and others link it to ``python3``.
    For disambiguation python, pip, and virtualenv shall mean their python v3 versions here, i.e. ``python3``, ``pip3``, ``virtualenv3``.

.. warning::

    You will need to have |git|_, and |python|_ installed for any of the below methods to work.
    You will also need |mongodb|_ if you intend to create a local database, (more than likely), but python-ezdb can still connect to already running databases without it if you happen to have one already.

This section will outline various methods for installation of python-ezdb, and its dependencies. Not all methods are equal there are slight variations between them, which are outlined in the respective sections below, along with instructions for each method:

.. contents:: :local:

.. _section_files-only:

Files-only/ development
+++++++++++++++++++++++

Automated
+++++++++

This section discusses the more automated and repeatable installation methods for Nemesyst, but they do not contain all the files needed to learn, and begin developing Nemesyst integrated applications, rather this includes just the bare-bones Nemesyst ready for your deployment.

pip
---

For now you can use pip via:

.. code-block:: bash

  pip install git+https://github.com/DreamingRaven/python-ezdb.git#branch=master

Archlinux
---------

Install `python-ezdb-git <https://aur.archlinux.org/packages/python-ezdb-git/>`_:sup:`AUR`.

Manual
++++++

This section outlines the manual methods of installing python-ezdb, for maximum control at the cost of time and repeatability.

setup.py
--------

.. code-block:: bash

  git clone https://github.com/DreamingRaven/python-ezdb
  cd python-ezdb
  python setup.py install


Archlinux
---------

.. code-block:: bash

  git clone https://github.com/DreamingRaven/python-ezdb
  cd python-ezdb/.archlinux/
  makepkg -si

.. _section_virtual-env:

Virtual env
-----------

To create the `python-virtualenv <https://wiki.archlinux.org/index.php/Python/Virtual_environment>`_:

.. code-block:: bash

    virtualenv venv

If python 3 is not the default python for your virtualenvironment, simply delete the new directory ``venv`` and instead use the following to generate a new one with python3:

.. code-block:: bash

     virtualenv -p python3 venv

To then use the newly created virtual environment:

.. code-block:: bash

    source venv/bin/activate

OR if you are using a terminal like fish:

.. code-block:: bash

    source venv/bin/activate.fish

To install Nemesyst and all its dependencies into a virtual environment while it is being used (activated):

.. code-block:: bash

    pip install git+https://github.com/DreamingRaven/python-ezdb.git#branch=master

To exit the virtual environment:

.. code-block:: bash

      deactivate
