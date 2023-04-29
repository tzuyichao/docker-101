FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libssl-dev libffi-dev

RUN pip install cryptography

RUN python -c "from cryptography.fernet import Fernet; key = Fernet.generate_key(); print(key.decode())"
