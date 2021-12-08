FROM python:3.8.12-slim-buster AS build

ARG TARGET=prod

ENV PYTHONUNBUFFERED=1 \
    PATH=/root/.local/bin:$PATH \
    PROCFILE_PATH=/app/Procfile \
    LC_ALL=C.UTF-8

RUN mkdir -p /usr/share/man/man1/ /usr/share/man/man7/

RUN apt-get update && apt-get upgrade -y

# Dependencies
RUN apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        gettext \
        libcap2-bin \
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
        postgresql-client-11 \
        wget \
        zlib1g

RUN if [ "$TARGET" = "dev" ] ; then apt-get install -y --no-install-recommends \
        build-essential \
        gcc \
        gfortran \
        libatlas-base-dev \
        libopenblas-dev \
        libffi-dev \
        libfreetype6-dev \
        libjpeg62-turbo-dev \
        liblapack-dev \
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
RUN pip install pip-reqs==0.10.0
RUN pip install start==0.2
# required for "pip compile" command in Python >= 3.8
RUN pip install pip-tools

RUN if [ "$TARGET" = "dev" ] ; then \
        pip install flit flit-core setuptools-scm poetry auditwheel \
   ; fi

COPY add_addons_dev_to_syspath.py /usr/local/lib/python3.8/site-packages/add_addons_dev_to_syspath.py
RUN echo 'import add_addons_dev_to_syspath' >/usr/local/lib/python3.8/site-packages/add_addons_dev_to_syspath.pth

# Cleanup
RUN apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /root/.cache

# Application environment setup
RUN mkdir -p /app /data
RUN useradd --create-home --user-group -u 1000 app


FROM scratch
COPY --from=build / /

# Execution environment setup
ENV LC_ALL=C.UTF-8 \
    NVM_DIR=/opt/nvm \
    PATH=/root/.local/bin:$PATH \
    PIP_REQUIRE_VIRTUALENV=false \
    PROCFILE_PATH=/app/Procfile \
    PYTHONUNBUFFERED=1 \
    WHEELS_PLATFORM=buster-py38
WORKDIR /app
EXPOSE 80/tcp 443/tcp
ENTRYPOINT ["/tini", "-g", "--"]
CMD ["start", "web"]
