FROM golang:latest as builder
ENV GO111MODULE=off

WORKDIR /myapp
COPY welcome.go .
RUN go build -o welcome .

FROM scratch
WORKDIR /myapp
COPY --from=builder /myapp/welcome .
ENTRYPOINT ["./welcome"]

