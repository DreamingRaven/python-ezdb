FROM ubuntu:20.10

# updating and installing basic ubuntu python container
RUN apt update && \
    apt install -y python3 python3-pip git

COPY . /ezdb

RUN cd /ezdb && \
    python3 ./setup.py install
