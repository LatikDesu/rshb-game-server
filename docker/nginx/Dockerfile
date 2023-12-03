FROM nginx:stable-alpine

RUN #rm /etc/nginx/conf.d/default.conf

ADD ./docker/nginx/nginx.conf /etc/nginx/conf.d/nginx.conf

EXPOSE 80
EXPOSE 443

CMD ["nginx-debug", "-g", "daemon off;"]