# hadolint global ignore=DL3059
FROM python:3.12.1-alpine3.19 AS build

ARG TARGET=prod
ARG TARGETARCH
ARG PIP_VERSION=23.3.1
ARG PIPREQS_VERSION=0.12.0
ARG START_VERSION=0.2

ENV PATH=/root/.local/bin:$PATH

RUN apk update && apk upgrade

# Dependencies
# hadolint ignore=DL3018
RUN apk add --no-cache \
        curl \
        freetype \
        gdal \
        gettext \
        jpeg \
        lcms2 \
        libffi \
        openssl \
        libwebp \
        libxml2 \
        libxslt \
        mailcap \
        openblas \
        openjpeg \
        pcre \
        postgresql-client \
        postgresql-libs \
        proj \
        tiff \
        tini \
        yaml

# hadolint ignore=DL3018
RUN if [ "$TARGET" = "dev" ] ; then apk add --no-cache \
        autoconf \
        automake \
        blas-dev \
        cairo-dev \
        cargo \
        cmake \
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
        openssl-dev \
        libwebp-dev \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        make \
        musl-dev \
        openblas-dev \
        openjpeg-dev \
        pcre-dev \
        pkgconf \
        postgresql-dev \
        proj-dev \
        readline-dev \
        tiff-dev \
        yaml-dev \
        zlib-dev \
    ; fi

# Python environment setup
# Note: pip 23.2.1 breaks pip-reqs
RUN pip install --no-cache-dir pip==${PIP_VERSION}
RUN pip install --no-cache-dir pip-reqs==${PIPREQS_VERSION}
RUN pip install --no-cache-dir start==${START_VERSION}

# TODO: Avoid the need for pip-tools
# hadolint ignore=DL3013
RUN if [ "$TARGET" = "dev" ] ; then \
        pip install --no-cache-dir pip-tools flit flit-core setuptools-scm poetry auditwheel \
   ; fi

COPY add_addons_dev_to_syspath.py /usr/local/lib/python3.12/site-packages/add_addons_dev_to_syspath.py
RUN echo 'import add_addons_dev_to_syspath' >/usr/local/lib/python3.12/site-packages/add_addons_dev_to_syspath.pth

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
    /etc/shadow-


FROM scratch
COPY --from=build / /

# Execution environment setup
RUN addgroup -S app && adduser -D -G app -u 1000 app
ENV WHEELS_PLATFORM=alpine319-py312 \
    PROCFILE_PATH=/app/Procfile \
    PATH=/root/.local/bin:$PATH
WORKDIR /app
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["start", "web"]
