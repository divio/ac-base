FROM python:3.6.2-alpine3.6 AS build

ARG TARGET=prod
ENV PATH=/root/.local/bin:$PATH

# Dependencies
RUN apk update
RUN apk del libressl2.5-libssl
RUN apk upgrade && apk add \
    curl \
    freetype \
    gettext \
    jpeg \
    lcms2 \
    libffi \
    libressl2.5-libtls \
    libwebp \
    libxml2 \
    libxslt \
    openjpeg \
    postgresql-libs \
    postgresql-client \
    tiff \
    tini \
    yaml
    # gdal not yet in 3.6
    # proj4 not yet in 3.6

RUN if [ "$TARGET" = "dev" ] ; then apk add \
        freetype-dev \
        gcc \
        g++ \
        gfortran \
        ghostscript-dev \
        imagemagick-dev \
        jpeg-dev \
        lapack-dev \
        lcms2-dev \
        libffi-dev \
        libwebp-dev \
        libressl-dev \
        libxml2-dev \
        libxslt-dev \
        linux-headers \
        musl-dev \
        openjpeg-dev \
        postgresql-dev \
        readline-dev \
        tiff-dev \
        yaml-dev \
        zlib-dev \
    ; fi
    # gdal-dev not yet in 3.6
    # libproj4-dev not yet in 3.6

# Python environment setup
RUN curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python
RUN /root/.local/venvs/pipsi/bin/pip install virtualenv
RUN ln -s /root/.local/venvs/pipsi/bin/virtualenv /root/.local/bin/virtualenv

RUN pipsi install pip-reqs==0.5
RUN pipsi install start==0.2
RUN if [ "$TARGET" = "dev" ] ; then pipsi install 'https://github.com/aldryncore/pip-tools/archive/1.9.0.1.tar.gz#egg=pip-tools==1.9.0.1' ; fi

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
