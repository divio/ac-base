FROM python:2.7.16-slim-stretch AS build

ARG TARGET=prod

ENV PYTHONUNBUFFERED=1 \
    PIP_REQUIRE_VIRTUALENV=false \
    WHEELS_PLATFORM=aldryn-baseproject-v4-py27 \
    PATH=/virtualenv/bin:/root/.local/bin:$PATH \
    PROCFILE_PATH=/app/Procfile \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    NVM_VERSION=0.33.5

COPY stack /stack/base
RUN DEBIAN_FRONTEND=noninteractive /stack/base/install.sh

FROM scratch
COPY --from=build / /

# Execution environment setup
# TODO: Remove NGINX_CONF_PATH once aldryn-django has been fixed to work
#       without it set.
ENV PYTHONUNBUFFERED=1 \
    PIP_REQUIRE_VIRTUALENV=false \
    WHEELS_PLATFORM=aldryn-baseproject-v4-py27 \
    PATH=/virtualenv/bin:/root/.local/bin:$PATH \
    PROCFILE_PATH=/app/Procfile \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    NVM_VERSION=0.33.5 \
    NGINX_CONF_PATH=""
WORKDIR /app
VOLUME /data
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/tini", "-g", "--"]
CMD ["start", "web"]
