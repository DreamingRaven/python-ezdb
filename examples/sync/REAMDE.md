# Automatic data pushing

To use first please modify sync/sync.py with credentials for the databases
in question, e.g usernames passwords hostnames etc.
A full list of options can be found here: https://python-ezdb.readthedocs.io/en/latest/mongo.html#ezdb.mongo.Mongo.connect

Once the file has been configured and all the files like any tls certificates stated in sync.py are copied adjacent to sync.py, you can run the script indefinateley by using the docker-compose file in this directory. Simply:
```
sudo docker-compose up --build -d
```
This will run in perpetuity. To stop it when it is no longer needed, from this directory simply invoke:
```
sudo docker-compose down
```
Thats it, its not complicated, I just put together this python + docker script to help illustrate the process/ exemplify some things python-ezdb can do.
