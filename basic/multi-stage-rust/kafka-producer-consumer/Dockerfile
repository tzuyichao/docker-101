# Build stage
FROM rust:latest AS build

WORKDIR /app

COPY . .

RUN cargo build --release

# Final stage
FROM debian:buster-slim

RUN apt-get -y update
RUN apt-get -y install openssl

WORKDIR /app

COPY --from=build /app/target/release/kafka-producer-consumer .

CMD ["./kafka-producer-consumer"]
