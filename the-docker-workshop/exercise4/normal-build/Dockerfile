FROM golang:latest
ENV GO111MODULE=off
WORKDIR /myapp
COPY welcome.go .
RUN go build -o welcome .
ENTRYPOINT ["./welcome"]