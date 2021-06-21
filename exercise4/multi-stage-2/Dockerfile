FROM openjdk:16.0.1-jdk-slim as builder

RUN apt-get update && apt-get install git -y
WORKDIR /myapp
RUN git clone https://github.com/tzuyichao/demo.git
RUN cd demo && chmod +x gradlew && ./gradlew build

ENTRYPOINT ["/bin/bash"]

FROM openjdk:16-alpine

WORKDIR /myapp
COPY --from=builder /myapp/demo/build/libs/demo-0.0.1-SNAPSHOT.jar .

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "/myapp/demo-0.0.1-SNAPSHOT.jar"]