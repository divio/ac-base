#!/bin/bash
#
# Prepares the "stack" to run apps and the environment to run buildpacks
#
set -x
set -e

PYTHON_MAJOR_VERSION=$(python -c 'import platform; print(platform.python_version_tuple()[0])')

SCRIPT=$(readlink -f "$0")
BASEDIR=$(dirname "$SCRIPT")

# Debian slim has some issue with some packages that try to install
# manpages into directories that don't exist (e.g postgresql-client).
# So we create those dirs here.
# https://github.com/debuerreotype/debuerreotype/issues/10
# Rumors have it that this will be fixed in the next debian version (buster).
mkdir -p /usr/share/man/man1/
mkdir -p /usr/share/man/man7/


# Update package listings
apt-get update

# Update system
apt-get upgrade -y

#
# SYSTEM PACKAGES
#
# Install packages
# xargs apt-get install -y --no-install-recommends < ${BASEDIR}/packages.txt
# The sed command removes comments and empty lines from the packages file.
cat ${BASEDIR}/packages.prod.txt | sed '/^#/ d' | sed '/^$/d' | xargs apt-get install -y --no-install-recommends

# If we're building the dev image install the dev packages
if [ "$TARGET" = "dev" ] ; then cat ${BASEDIR}/packages.dev.txt | sed '/^#/ d' | sed '/^$/d' | xargs apt-get install -y --no-install-recommends ; fi

#
# MISC
#

pip install pip-reqs==0.8.0
pip install start==0.2
pip install virtualenv

# TODO: Avoid the need for pip-tools
if [ "$TARGET" = "dev" ] ; then \
        wget https://raw.githubusercontent.com/mitsuhiko/pipsi/master/get-pipsi.py && \
        python get-pipsi.py --no-modify-path && \
        rm get-pipsi.py && \
        ln -s /root/.local/venvs/pipsi/bin/virtualenv /root/.local/bin/virtualenv && \
        pipsi install 'https://github.com/aldryncore/pip-tools/archive/1.9.0.2.tar.gz#egg=pip-tools==1.9.0.2' \
   ; fi

# tini: minimal PID 1 init. reaps zombie processes and forwards signals.
# set
# ENTRYPOINT ["/tini", "--"]
# in the Dockerfile to make it the default method for starting processes.
# https://github.com/krallin/tini
curl -L --show-error --retry 5 -o /tini https://github.com/krallin/tini/releases/download/v0.18.0/tini
chmod +x /tini

# workaround for a bug in hub.docker.com
ln -s -f /bin/true /usr/bin/chfn

# install custom commands
cp ${BASEDIR}/run-forest-run /usr/local/bin/run-forest-run

# default virtualenv
# NOTE: PATH=/virtualenv/bin:$PATH must be set in the Dockerfile
virtualenv --no-site-packages /virtualenv

# Install nvm
${BASEDIR}/nvm.sh

# Add all directories in /app/addons-dev to the PYTHONPATH
cp ${BASEDIR}/add_addons_dev_to_syspath.py ${PYTHON_SITE_PACKAGES_ROOT}/add_addons_dev_to_syspath.py
cp ${BASEDIR}/add_addons_dev_to_syspath.pth ${PYTHON_SITE_PACKAGES_ROOT}/add_addons_dev_to_syspath.pth

# setup virtualenv
virtualenv --no-site-packages /virtualenv

# Prepate /app directory
mkdir -p /app && mkdir -p /data

# Add a dummy Procfile
echo 'web: echo "Define your own scripts here"' > /app/Procfile

# Cleanup
apt-get autoremove -y
apt-get clean
rm -rf /var/lib/apt/lists/*
rm -rf /tmp/*
