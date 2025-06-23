FROM nginx:alpine

RUN mkdir -p /etc/nginx/conf.d/
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Создаём директорию для статики и копируем файлы
RUN mkdir -p /usr/share/nginx/html/static
COPY styles.css /usr/share/nginx/html/static

EXPOSE 80