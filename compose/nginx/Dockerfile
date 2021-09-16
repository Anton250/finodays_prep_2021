FROM openresty/openresty:latest

COPY ./compose/nginx/nginx.conf /etc/openresty/nginx.conf
COPY ./compose/nginx/parrotdocx.conf /etc/nginx/conf.d/parrotdocx.conf

ENV TZ=Europe/Moscow
