FROM nginx:1.25.3-alpine

ARG CONFIG
COPY $CONFIG /etc/nginx/conf.d/default.conf

ENTRYPOINT ["nginx","-g","daemon off;"]
