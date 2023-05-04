FROM ubuntu:lunar

RUN apt update && apt install -y wget

RUN wget https://github.com/prometheus/node_exporter/releases/download/v1.5.0/node_exporter-1.5.0.linux-amd64.tar.gz

RUN tar xvfz node_exporter-1.5.0.linux-amd64.tar.gz

EXPOSE 9100:9100

CMD ["./node_exporter-1.5.0.linux-amd64/node_exporter"]

