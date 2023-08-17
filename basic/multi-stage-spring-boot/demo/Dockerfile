FROM gradle:jdk17 as builder

WORKDIR /app

COPY . .

RUN gradle clean build

FROM mcr.microsoft.com/java/jdk:17-zulu-alpine

WORKDIR /app

COPY --from=builder /app/build/libs/demo-0.0.1-SNAPSHOT.jar /app/app.jar

EXPOSE 8088

CMD ["java", "-jar", "app.jar"]