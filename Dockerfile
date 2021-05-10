FROM python:3.8-alpine
WORKDIR /flask-server/

# Only copy requirements.txt at this stage, to avoid long rebuilds when the source changes.
COPY requirements.txt /flask-server/requirements.txt
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Now we copy in the code and check that the tests pass.
COPY . /flask-server/
WORKDIR /flask-server/test/unit
RUN PYTHONPATH=/flask-server/src/ pytest

# Potential improvement: Use a multi-stage build to remove build artifacts and testing libraries.

# Tests passed, run the server!
WORKDIR /flask-server/src
CMD ["python3", "server.py"]
