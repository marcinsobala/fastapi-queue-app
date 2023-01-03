FROM python:3.11.0-slim-buster

RUN apt-get update  && \
    apt-get install -y --no-install-recommends \
    python3-dev  \
    libpq-dev

RUN pip install --upgrade pip

COPY requirements.txt ./
RUN pip install -r ./requirements.txt && \
    rm -rf ./requirements.txt

WORKDIR /app

COPY . /app
ENV PYTHONPATH=/app