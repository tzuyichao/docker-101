FROM postgres:16

USER root

RUN apt-get update && apt-get install -y \
    python3 python3-venv python3-pip \
    ca-certificates curl \
    && update-ca-certificates \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m venv /opt/venv

RUN /opt/venv/bin/pip install --no-cache-dir -U pip setuptools wheel && \
    /opt/venv/bin/pip install --no-cache-dir --prefer-binary \
      "patroni[zookeeper,psycopg2-binary]==4.1.0"

ENV PATH="/opt/venv/bin:${PATH}"

USER postgres
EXPOSE 5432 8008
ENTRYPOINT ["patroni"]
