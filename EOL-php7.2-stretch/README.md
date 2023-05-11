# PHP base images for Divio Cloud

This repository contains the docker base images for the Divio cloud PHP support.
The images are based on the official PHP docker images extended by typical
requirements of the major frameworks supported in Divio Cloud.
If you need smaller images that do not need to compile frontend requirements,
you might want to fork our images and drop support for some extensions.

## contents

These images install the following PHP extensions and libs:

_bcmath, bz2, calendar, exif, iconv, intl, mbstring, opcache, pcntl, pdo_pgsql,
pgsql, soap, xml, xmlrpc, zip, imagemagick, libfreetype6-dev, libicu-dev,
libjpeg-dev, libkrb5-dev, libldap2-dev, libmagickwand-dev, libmemcached-dev,
libmemcachedutil2, libpng-dev, libpq-dev, libssl-dev, libxml2-dev, libzip-dev_

Also included are `nvm (v0.34.0)` to install custom `npm` and `nodejs` versions
as well as `yarn (v1.17)` to compile the webpack requirements.
