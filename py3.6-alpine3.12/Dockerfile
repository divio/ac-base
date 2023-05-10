# hadolint global ignore=DL3059
FROM python:3.6.11-alpine3.12 AS build

ARG TARGET=prod
ENV PATH=/root/.local/bin:$PATH

RUN apk update && apk upgrade

# Dependencies
RUN apk add \
        curl \
        freetype \
        gdal \
        gettext \
        jpeg \
        lcms2 \
        libffi \
        libressl3.1-libtls \
        libwebp \
        libxml2 \
        libxslt \
        mailcap \
        openjpeg \
        pcre \
        postgresql-client \
        postgresql-libs \
        proj \
        tiff \
        tini \
        yaml

RUN if [ "$TARGET" = "dev" ] ; then apk add \
        blas-dev \
        freetype-dev \
        g++ \
        gcc \
        gdal-dev \
        gfortran \
        ghostscript-dev \
        imagemagick-dev \
        jpeg-dev \
        lapack-dev \
        lcms2-dev \
        libffi-dev \
        libressl-dev \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        make \
        musl-dev \
        openjpeg-dev \
        pcre-dev \
        postgresql-dev \
        proj-dev \
        readline-dev \
        tiff-dev \
        yaml-dev \
        zlib-dev \
    ; fi

# Python environment setup
RUN pip install --no-cache-dir pip-reqs==0.9.0
RUN pip install --no-cache-dir start==0.2

# TODO: Avoid the need for pip-tools
RUN if [ "$TARGET" = "dev" ] ; then \
        curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python && \
        /root/.local/venvs/pipsi/bin/pip --no-cache-dir install virtualenv && \
        ln -s /root/.local/venvs/pipsi/bin/virtualenv /root/.local/bin/virtualenv && \
        pipsi install 'https://github.com/aldryncore/pip-tools/archive/1.9.0.2.tar.gz#egg=pip-tools==1.9.0.2' \
   ; fi

COPY add_addons_dev_to_syspath.py /usr/local/lib/python3.6/site-packages/add_addons_dev_to_syspath.py
RUN echo 'import add_addons_dev_to_syspath' >/usr/local/lib/python3.6/site-packages/add_addons_dev_to_syspath.pth
# Workaround for stack size issues on musl-c, see the following URL for details:
# https://github.com/voidlinux/void-packages/issues/4147
RUN echo 'import threading; threading.stack_size(8 * 1024 ** 2)' >/usr/local/lib/python3.6/site-packages/set_threads_stack_size.pth

# Cleanup
RUN rm -rf /root/.cache

# Application environment setup
RUN mkdir -p /app

# The group of the following files has to be changed to root for multistage
# builds to work with userns remapping enabled. This is a bug in the Docker
# legacy builder: https://github.com/moby/moby/issues/34645

# Initially belonging to group shadow
RUN chgrp root \
    /etc/shadow \
    /etc/shadow.apk-new


FROM scratch
COPY --from=build / /

# Execution environment setup
ENV WHEELS_PLATFORM=alpine312-py36 \
    PROCFILE_PATH=/app/Procfile \
    PATH=/root/.local/bin:$PATH
WORKDIR /app
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["start", "web"]
