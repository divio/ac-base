FROM python:3.6.8-alpine3.8 AS build

ARG TARGET=prod
ENV PATH=/root/.local/bin:$PATH

# Add edge packages
RUN echo @edge http://nl.alpinelinux.org/alpine/edge/main >> /etc/apk/repositories
RUN echo @edge http://nl.alpinelinux.org/alpine/edge/testing >> /etc/apk/repositories
RUN echo @edge http://nl.alpinelinux.org/alpine/edge/community >> /etc/apk/repositories
RUN apk update && apk upgrade

# Dependencies
RUN apk add \
        curl \
        freetype \
        gdal@edge \
        gettext \
        jpeg \
        lcms2 \
        libffi \
        libressl2.7-libtls \
        libwebp \
        libxml2 \
        libxslt \
        mailcap \
        openjpeg \
        pcre \
        postgresql-client \
        postgresql-libs \
        proj@edge \
        tiff \
        tini \
        yaml

RUN if [ "$TARGET" = "dev" ] ; then apk add \
        freetype-dev \
        g++ \
        gcc \
        gdal-dev@edge \
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
        proj-dev@edge \
        readline-dev \
        tiff-dev \
        yaml-dev \
        zlib-dev \
    ; fi

# Python environment setup
RUN pip install pip-reqs==0.8.5
RUN pip install start==0.2

# TODO: Avoid the need for pip-tools
RUN if [ "$TARGET" = "dev" ] ; then \
        curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python && \
        /root/.local/venvs/pipsi/bin/pip install virtualenv && \
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


FROM scratch
COPY --from=build / /

# Execution environment setup
ENV WHEELS_PLATFORM=alpine38-py36 \
    PROCFILE_PATH=/app/Procfile \
    PATH=/root/.local/bin:$PATH
WORKDIR /app
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["start", "web"]
