FROM node:10-slim AS builder

ARG VUE_APP_WEB3_ENDPOINT

RUN apt update
RUN apt install -y make gcc g++ python

WORKDIR /build
COPY . .
RUN yarn
RUN yarn run build

FROM nginx:1.17.3-alpine
COPY --from=builder /build/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx/api_proxy.conf /etc/nginx/api_proxy.conf
COPY nginx/run.sh /
CMD ["/run.sh"]
