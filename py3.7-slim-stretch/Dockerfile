FROM python:3.7.8-slim-stretch AS build

ARG TARGET=prod

ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    PROCFILE_PATH=/app/Procfile \
    LC_ALL=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    NVM_VERSION=0.33.11

RUN mkdir -p /usr/share/man/man1/ /usr/share/man/man7/

RUN apt-get update && apt-get upgrade -y

# Dependencies
RUN apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gettext \
        libffi6 \
        libfreetype6 \
        libjpeg62-turbo \
        libopenjp2-7 \
        libpcre3 \
        libssl1.1 \
        libtiff5 \
        libxslt1.1 \
        libyaml-0-2 \
        mime-support \
        postgresql-client-9.6 \
        wget \
        zlib1g

RUN if [ "$TARGET" = "dev" ] ; then apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        libffi-dev \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        liblcms2-dev \
        libopenjp2-7-dev \
        libpcre3-dev \
        libpq-dev \
        libssl-dev \
        libtiff-dev \
        libwebp-dev \
        libxslt-dev \
        libyaml-dev \
        zlib1g-dev \
    ; fi

# Workaround for a bug in hub.docker.com
RUN ln -s -f /bin/true /usr/bin/chfn

# Install tini
RUN curl -L --show-error --retry 5 -o /tini https://github.com/krallin/tini/releases/download/v0.18.0/tini
RUN chmod +x /tini

# Python environment setup
RUN pip install pip-reqs==0.8.6
RUN pip install start==0.2

# TODO: Avoid the need for pip-tools
RUN if [ "$TARGET" = "dev" ] ; then \
        curl https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py | python && \
        /root/.local/venvs/pipsi/bin/pip install virtualenv && \
        ln -s /root/.local/venvs/pipsi/bin/virtualenv /root/.local/bin/virtualenv && \
        pipsi install 'https://github.com/aldryncore/pip-tools/archive/1.9.0.2.tar.gz#egg=pip-tools==1.9.0.2' \
   ; fi

COPY add_addons_dev_to_syspath.py /usr/local/lib/python3.7/site-packages/add_addons_dev_to_syspath.py
RUN echo 'import add_addons_dev_to_syspath' >/usr/local/lib/python3.7/site-packages/add_addons_dev_to_syspath.pth

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

# Cleanup
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Application environment setup
RUN mkdir -p /app /data


FROM scratch
COPY --from=build / /

# Execution environment setup
ENV LC_ALL=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    PATH=/root/.local/bin:$PATH \
    PIP_REQUIRE_VIRTUALENV=false \
    PROCFILE_PATH=/app/Procfile \
    PYTHONUNBUFFERED=1 \
    WHEELS_PLATFORM=stretch-py37
WORKDIR /app
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/tini", "-g", "--"]
CMD ["start", "web"]
