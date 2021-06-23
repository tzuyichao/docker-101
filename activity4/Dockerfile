FROM golang:1.14.2-alpine AS builder

COPY main.go .
RUN go env -w GO111MODULE=auto
RUN go build -o /main

FROM alpine:latest

WORKDIR /myapp
COPY --from=builder /main .
RUN chmod +x /myapp/main

RUN adduser -D myuser && chown -R myuser /myapp
USER myuser

EXPOSE 8080

ENTRYPOINT ["/myapp/main"]
