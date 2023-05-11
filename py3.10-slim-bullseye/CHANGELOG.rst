Changelog
=========

1.5 (2023-05-11)
----------------

* Upgraded Python to 3.9.16.
* Added support for `cmake`, `pkg-config`, `autotools`, and `libcairo2`.
* Upgraded pip to 23.1.2.
* Upgraded pip-reqs to 0.11.0.
* Added support for multi-arch builds.


1.4 (2023-01-06)
----------------

* Upgraded Python base image version to 3.10.9.


1.3 (2022-08-19)
----------------

* Upgraded Python base image version to 3.10.6.


1.2 (2022-08-11)
----------------

* Added a workaround for a Docker bug causing multistage builds to fail when
  userns remapping is enabled.


1.1 (2022-03-08)
----------------

* Added WHEELS_PLATFORM environment variable again.


1.0 (2022-02-30)
----------------

* Initial release of Python 3.10 / Debian Bullseye base image.
