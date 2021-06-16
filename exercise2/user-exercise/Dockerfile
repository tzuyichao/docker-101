FROM ubuntu
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install apache2 -y
USER www-data
CMD ["whoami"]