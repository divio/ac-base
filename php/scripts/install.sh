#!/bin/bash

set -euf -o pipefail

echo "force-unsafe-io" > /etc/dpkg/dpkg.cfg.d/02apt-speedup
echo "Acquire::http {No-Cache=True;};" > /etc/apt/apt.conf.d/no-cache

DEBIAN_FRONTEND=noninteractive
  dpkg-reconfigure -f noninteractive tzdata \
  && apt-get update \
  && apt-get upgrade -y \
  &&  DEBIAN_FRONTEND=noninteractive apt-get install -yqq \
      apt-transport-https \
      apt-utils \
      build-essential \
      curl \
      dumb-init \
      gnupg2 \
      libc-client-dev \
      nginx \
      openssh-client \
      unzip \
      zlib1g-dev \
      --no-install-recommends \
  && rm -rf /var/lib/apt/lists/*

buildDependencies=" \
libbz2-dev \
libsasl2-dev \
"

runtimeDependencies=" \
imagemagick \
libfreetype6-dev \
libicu-dev \
libjpeg-dev \
libkrb5-dev \
libldap2-dev \
libmagickwand-dev \
libmemcached-dev \
libmemcachedutil2 \
libpng-dev \
libpq-dev \
libssl-dev \
libxml2-dev \
libzip-dev \
"

extensions=" \
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
pgsql \
soap \
xml \
xmlrpc \
zip
"

apt-get update && DEBIAN_FRONTEND=noninteractive apt-get -yqq install $buildDependencies --no-install-recommends \
  && DEBIAN_FRONTEND=noninteractive apt-get -yqq install $runtimeDependencies --no-install-recommends \
  && rm -rf /var/lib/apt/lists/* \
  && docker-php-ext-install -j$(nproc) $extensions \
  && docker-php-ext-configure gd --with-freetype-dir=/usr/include/ --with-jpeg-dir=/usr/include/ \
  && docker-php-ext-install -j$(nproc) gd \
  && docker-php-ext-configure ldap --with-libdir=lib/x86_64-linux-gnu/ \
  && docker-php-ext-install -j$(nproc) ldap \
  && docker-php-ext-configure imap --with-kerberos --with-imap-ssl \
  && docker-php-ext-install -j$(nproc) imap

docker-php-source extract \
  && curl -L -s https://github.com/php-memcached-dev/php-memcached/archive/v3.1.3.zip -o /tmp/php-memcached-3.1.3.zip \
  && unzip /tmp/php-memcached-3.1.3.zip -d /tmp \
  && mv /tmp/php-memcached-3.1.3 /usr/src/php/ext/memcached \
  && docker-php-ext-install memcached \
  && docker-php-ext-enable memcached \
  && docker-php-source delete

pecl channel-update pecl.php.net \
  && pecl install imagick redis xdebug \
  && docker-php-ext-enable imagick redis xdebug

echo "memory_limit=1G" > /usr/local/etc/php/conf.d/zz-conf.ini

curl -sL https://deb.nodesource.com/setup_12.x | bash - \
    && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -yqq install nodejs yarn --no-install-recommends \
    && npm i -g npm

apt-get purge -y --auto-remove $buildDependencies

curl -O https://bin.equinox.io/c/ekMN3bCZFUn/forego-stable-linux-amd64.tgz \
    && tar xf forego-stable-linux-amd64.tgz \
    && rm forego-stable-linux-amd64.tgz \
    && mv forego /usr/local/bin/forego
