## Activity 1.01 ~ 1.02

docker run -d -e POSTGRES_USER=panoramic -e POSTGRES_PASSWORD=trekking --name postgres1 postgres:latest

docker run -e POSTGRES_USER=panoramic -e POSTGRES_PASSWORD=trekking --name postgres1 postgres:latest

docker exec -it postgres1 /bin/bash

psql --username panoramic --password

