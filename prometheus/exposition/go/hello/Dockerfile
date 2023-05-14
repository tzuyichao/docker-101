# builder
FROM golang:1.20.4-alpine as builder
WORKDIR /hello
COPY . .
RUN go env -w GO111MODULE=auto
RUN go build

# app
FROM alpine

EXPOSE 8000:8000
WORKDIR /entry
COPY --from=builder /hello/hello .
RUN chmod +x hello

CMD ["/entry/hello"]