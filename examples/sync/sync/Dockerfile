FROM python:3-alpine

copy requirements.txt ./sync/requirements.txt
RUN apk --no-cache add git musl-dev linux-headers g++ && \
    pip3 install --no-cache-dir -r ./sync/requirements.txt
COPY . ./sync/.
WORKDIR ./sync/

CMD ["python", "./sync.py"]
