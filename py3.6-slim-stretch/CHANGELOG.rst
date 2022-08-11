Changelog
=========


4.19 (2022-08-11)
----------------

* Added a workaround for a Docker bug causing multistage builds to fail when
  userns remapping is enabled.


4.18 (2020-07-16)
-----------------

* Upgrade to pip-reqs 0.8.6.


4.17 (2020-07-07)
-----------------

* Bumped Python base image to version 3.6.11.


4.16 (2020-04-10)
-----------------

* Build logs to multiple lines.


4.15 (2019-04-16)
-----------------

* Fix issue with loading addons-dev


4.14 (2019-03-28)
-----------------

* Add mime-support package


4.13 (2019-03-28)
-----------------

* Upgrade to pip-reqs 0.8.0.
* Upgrade to NVM 0.33.11.
* Install pipsi and pip-tools only in the dev build.
* Remove NGINX_CONF_PATH environment variable.
* Update Dockerfile to get rid of /stack scripts.


4.12 (2019-03-27)
----------------

* Upgrade to pip-reqs 0.7.2.


4.11 (2019-01-03)
-----------------

* Upgrade to Python 3.6.8.


4.10 (2018-08-20)
-----------------

* Upgrade pip-reqs to 0.6.
* Upgrade pip-tools to 1.9.0.2.
* Upgrade tini to 0.18.0.


4.9 (2018-08-14)
----------------

* Introduce a CHANGELOG.
* Upgrade to Python 3.6.6.
* Upgrade system to latest available packages.
