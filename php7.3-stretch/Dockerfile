FROM php:7.3-fpm-stretch AS build

ENV PATH=/root/.local/bin:$PATH \
    DEBIAN_FRONTEND=noninteractive \
    LC_ALL=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    NVM_VERSION=0.34.0 \
    MEMCACHE_VERSION=3.1.3

ENV BUILD_DEPENDENCIES=" \
    libbz2-dev \
    libsasl2-dev \
    "

ENV RUNTIME_DEPENDENCIES=" \
    imagemagick \
    libfreetype6-dev \
    libicu-dev \
    libjpeg62-turbo-dev \
    libjpeg-dev \
    libkrb5-dev \
    libldap2-dev \
    libmagickwand-dev \
    libmemcached-dev \
    libmemcachedutil2 \
    libpng-dev \
    libpq-dev \
    libssl-dev \
    libwebp-dev \
    libxml2-dev \
    libxpm-dev \
    libzip-dev \
    "

ENV EXTENSIONS=" \
    bcmath \
    bz2 \
    calendar \
    exif \
    iconv \
    intl \
    mbstring \
    opcache \
    pcntl \
    pdo_pgsql \
    pdo_mysql \
    pgsql \
    soap \
    xml \
    xmlrpc \
    zip \
    "

USER root

RUN echo "force-unsafe-io" > /etc/dpkg/dpkg.cfg.d/02apt-speedup
RUN echo "Acquire::http {No-Cache=True;};" > /etc/apt/apt.conf.d/no-cache

RUN dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update && apt-get upgrade -y \
  && apt-get install -yqq apt-transport-https apt-utils build-essential curl dumb-init gnupg2 libc-client-dev nginx openssh-client unzip zlib1g-dev --no-install-recommends \
  && apt-get -yqq install $BUILD_DEPENDENCIES --no-install-recommends \
  && apt-get -yqq install $RUNTIME_DEPENDENCIES --no-install-recommends \
  && docker-php-ext-install -j$(nproc) $EXTENSIONS \
  && docker-php-ext-configure gd --with-gd --with-webp-dir --with-jpeg-dir \
    --with-png-dir --with-zlib-dir --with-xpm-dir --with-freetype-dir \
  && docker-php-ext-install -j$(nproc) gd \
  && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
  && docker-php-ext-install -j$(nproc) ldap \
  && docker-php-ext-configure imap --with-kerberos --with-imap-ssl \
  && docker-php-ext-install -j$(nproc) imap

RUN docker-php-source extract \
  && curl -L -s https://github.com/php-memcached-dev/php-memcached/archive/v$MEMCACHE_VERSION.zip -o /tmp/php-memcached-$MEMCACHE_VERSION.zip \
  && unzip /tmp/php-memcached-$MEMCACHE_VERSION.zip -d /tmp \
  && mv /tmp/php-memcached-$MEMCACHE_VERSION /usr/src/php/ext/memcached \
  && docker-php-ext-install memcached \
  && docker-php-ext-enable memcached \
  && docker-php-source delete

RUN pecl channel-update pecl.php.net \
  && pecl install imagick redis xdebug \
  && docker-php-ext-enable imagick redis xdebug

RUN echo "memory_limit=1G" > /usr/local/etc/php/conf.d/zz-conf.ini
RUN mv "$PHP_INI_DIR/php.ini-production" "$PHP_INI_DIR/php.ini"

# Install nvm
# This base project ships with nvm only. Node and NPM can
# be installed in boilerplate using the following commands
#
#    ENV NODE_VERSION=0.12.14 \
#        NPM_VERSION=2.15.5
#    RUN source $NVM_DIR/nvm.sh && \
#        nvm install $NODE_VERSION && \
#        nvm alias default $NODE_VERSION && \
#        nvm use default && \
#        npm install -g npm@"$NPM_VERSION" && \
#        npm cache clear
#   ENV NODE_PATH=$NVM_DIR/versions/node/v$NODE_VERSION/lib/node_modules \
#       PATH=$NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
RUN mkdir -p $NVM_DIR
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v$NVM_VERSION/install.sh | bash

# Install yarn in addition
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get -yqq install yarn --no-install-recommends

RUN curl -O https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.tgz \
    && tar xf forego-stable-linux-amd64.tgz \
    && rm forego-stable-linux-amd64.tgz \
    && mv forego /usr/local/bin/forego

# Cleanup
RUN apt-get purge -y --auto-remove $BUILD_DEPENDENCIES

RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    apt-utils \
    autoconf \
    build-essential \
    dpkg-dev \
    file \
    libc-client-dev \
    libc-dev \
    libpcre3-dev \
    pkg-config \
    re2c

RUN apt-get autoremove -y && apt-get autoclean -y
RUN rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/man /usr/share/doc /usr/share/doc-base /root/.cache

# Copy composer binaries from official image
WORKDIR /composer

COPY --from=composer:1 /usr/bin/composer /usr/bin/composer

RUN mkdir -p /var/www/html \
    && composer global require "hirak/prestissimo:^0.3" \
    && rm -rf ~/.composer/cache/*

RUN ln -sf /dev/stdout /var/log/nginx/access.log \
    && ln -sf /dev/stderr /var/log/nginx/error.log

COPY ./vhost.conf /etc/nginx/sites-available/default

FROM scratch
COPY --from=build / /

ENV LC_ALL=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    PROCFILE_PATH=/app/Procfile \
    PATH=/root/.local/bin:$PATH

WORKDIR /app
EXPOSE 80/tcp
ENTRYPOINT ["docker-php-entrypoint"]
CMD ["php-fpm"]
