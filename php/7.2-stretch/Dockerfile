FROM php:7.2-fpm
EXPOSE 80

USER root

WORKDIR /composer

# COPY INSTALL SCRIPTS
COPY --from=composer:1 /usr/bin/composer /usr/bin/composer
COPY ./scripts/*.sh /composer/
RUN chmod a+x /composer/*.sh

# Install
RUN bash ./install.sh \
    && bash ./clean.sh \
    && mkdir -p /var/www/html \
    && composer global require "hirak/prestissimo:^0.3" \
    && rm -rf ~/.composer/cache/* \
    && ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY ./configs/nginx/vhost.conf /etc/nginx/sites-available/default

WORKDIR /app
