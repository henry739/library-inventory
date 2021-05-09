FROM python:3.8-alpine

COPY . /flask-server/
WORKDIR /flask-server/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

WORKDIR /flask-server/src
CMD ["python3", "server.py"]
