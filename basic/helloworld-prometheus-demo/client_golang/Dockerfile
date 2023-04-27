FROM golang:1.20.0-alpine

RUN apk update && apk upgrade && apk add bash git

WORKDIR /go/src/app

RUN git clone https://github.com/prometheus/client_golang.git && \
    cd client_golang/examples/random && go get -d && go build

CMD ["/go/src/app/client_golang/examples/random/random", "-listen-address=:8080"]