FROM ubuntu:latest

RUN apt-get update && apt-get install -y ssh iputils-ping python3 python3-pip

CMD ["python3", "-m", "http.server", "8000"]