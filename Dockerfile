FROM python:3.8-alpine

COPY . /flask-server/
WORKDIR /flask-server/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python3", "src/server.py"]
