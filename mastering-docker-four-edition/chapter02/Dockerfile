FROM alpine:latest
LABEL maintainer="Russ <russ@mckendrick.io>"
LABEL description="This example Dockerfile install NGINX."
RUN apk add --update nginx && \
    rm -rf /var/cache/apk/* && \
    mkdir -p /tmp/nginx/
COPY files/nginx.conf /etc/nginx/nginx.conf
COPY files/default.conf /etc/nginx/conf.d/default.conf
ADD https://raw.githubusercontent.com/PacktPublishing/Mastering-Docker-Fourth-Edition/master/chapter02/dockerfile-example/files/html.tar.gz /usr/share/nginx
EXPOSE 80/tcp
ENTRYPOINT ["nginx"]
CMD ["-g", "daemon off;"]