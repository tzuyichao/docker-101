# Build stage
FROM rust:latest AS build

WORKDIR /app

COPY . .

RUN cargo build --release

# Final stage
FROM debian:buster-slim

WORKDIR /app

COPY --from=build /app/target/release/minimal-warp .

EXPOSE 8000:8000

CMD ["./minimal-warp"]
