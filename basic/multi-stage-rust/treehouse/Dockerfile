# Build stage
FROM rust:latest AS build

WORKDIR /app

COPY . .

RUN cargo build --release

# Final stage
FROM debian:buster-slim

WORKDIR /app

COPY --from=build /app/target/release/threehouse .

CMD ["./threehouse"]
