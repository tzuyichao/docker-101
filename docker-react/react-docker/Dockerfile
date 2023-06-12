# https://www.knowledgehut.com/blog/web-development/how-to-dockerize-react-app
FROM node:20.3.0-slim as builder
WORKDIR /app
COPY package.json .
COPY yarn.lock .
RUN yarn install 
COPY . .
RUN yarn build

FROM nginx:1.19.0-alpine
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=builder /app/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]