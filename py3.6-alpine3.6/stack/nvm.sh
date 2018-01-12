#!/bin/bash
apk add -U curl bash ca-certificates openssl ncurses coreutils python2 make gcc g++ libgcc linux-headers grep util-linux binutils findutils
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.8/install.sh | bash
