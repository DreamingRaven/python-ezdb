FROM python:3-alpine

ARG workdir=/ezdb-stress

RUN mkdir -p ${workdir}

copy requirements.txt ${workdir}/requirements.txt

RUN apk --no-cache add git musl-dev linux-headers g++ && \
    pip3 install --no-cache-dir -r ${workdir}/requirements.txt

COPY . ${workdir}/.

WORKDIR ${workdir}

ENTRYPOINT ["python", "stress.py"]

CMD ["-h"]
