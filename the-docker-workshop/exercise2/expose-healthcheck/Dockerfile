FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install apache2 curl -y
HEALTHCHECK CMD curl -f http://localhost/ || exit 1
EXPOSE 80
ENTRYPOINT ["apache2ctl", "-D", "FOREGROUND"]