FROM python:3.6.8-alpine3.6 AS build

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
        libressl2.5-libtls \
        libwebp \
        libxml2 \
        libxslt \
        mailcap \
        openjpeg \
        pcre \
        postgresql-client \
        postgresql-libs \
        proj4@edge \
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
        proj4-dev@edge \
        readline-dev \
        tiff-dev \
        yaml-dev \
        zlib-dev \
    ; fi

# Python environment setup
RUN curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python
RUN /root/.local/venvs/pipsi/bin/pip install virtualenv
RUN ln -s /root/.local/venvs/pipsi/bin/virtualenv /root/.local/bin/virtualenv

RUN pipsi install pip-reqs==0.7.2
# `start` has no requirements, install through pip instead of pipsi to save
# some space by avoiding to setup a full virtualenv.
RUN pip install start==0.2
RUN if [ "$TARGET" = "dev" ] ; then pipsi install 'https://github.com/aldryncore/pip-tools/archive/1.9.0.2.tar.gz#egg=pip-tools==1.9.0.2' ; fi

COPY add_addons_dev_to_syspath.py /usr/local/lib/python3.6/site-packages/add_addons_dev_to_syspath.py
RUN echo 'import add_addons_dev_to_syspath' >/usr/local/lib/python3.6/site-packages/add_addons_dev_to_syspath.pth

# Cleanup
RUN rm -rf /root/.cache

# Application environment setup
RUN mkdir -p /app


FROM scratch
COPY --from=build / /

# Execution environment setup
ENV WHEELS_PLATFORM=alpine36-py36 \
    PROCFILE_PATH=/app/Procfile \
    PATH=/root/.local/bin:$PATH \
    NGINX_CONF_PATH=/dev/null
WORKDIR /app
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/sbin/tini", "--"]
CMD ["start", "web"]
