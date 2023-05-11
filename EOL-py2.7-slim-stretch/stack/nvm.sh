#!/bin/bash

#
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

curl -o- https://raw.githubusercontent.com/creationix/nvm/v$NVM_VERSION/install.sh | bash
