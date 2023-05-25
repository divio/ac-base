Changelog
=========


2023-05-24
----------

* Removed `--arch` param from `./build.py` in favor of Docker's
  `DOCKER_DEFAULT_PLATFORM` environment variable.


2023-05-11
----------

* Moved from GitHub+Docker Hub to Gitlab for building images.
* Added `easy_thumbnails[svg]` to the tested packages.
* Added `--arch` param in `./build.py` command.
* Added `--no-cache` flag in `docker build` command.
