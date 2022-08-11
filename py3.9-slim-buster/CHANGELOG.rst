Changelog
=========


2.2 (2022-08-11)
----------------

* Added a workaround for a Docker bug causing multistage builds to fail when
  userns remapping is enabled.


2.2 (2021-07-02)
----------------

* Upgrade Python to 3.9.6.
* Upgrade pip-reqs to 0.10.0 (fixes compatibility issues with pip).


2.1 (2020-12-30)
----------------

* Upgrade pip-reqs to 0.9.0


2.0 (2020-12-29)
----------------

* Upgrade Python to 3.9.1
* Replace forked pip-tools with upstream
* Install development libraries to deal with wheel building
* Drop nvm from the image
* Add a default user (without setting it as the container user)
* Add libcap binaries


1.0 (2020-11-03)
----------------

* Initial release of Python 3.9 / Debian Buster base image.
