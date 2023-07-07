FROM python:latest

RUN apt-get update

RUN pip install kafka-utils

COPY ./data/delta.yaml /etc/kafka_discovery/delta.yaml

