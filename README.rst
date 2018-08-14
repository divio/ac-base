divio/base
==========

Base images for Python projects deployed on Divio Cloud.


Locally build an image
----------------------

To locally build an image, run the following command::

   ./build.py --repo divio/base --tag 0.00-py3.6-alpine3.7 build

Check `./build.py --help` for additional information.


Release process
---------------

Tag commits with the desired Docker image tag, in the form::

   git tag <version>-<flavour>

Then push the tags to GitHub to trigger an automatic build on Docker Cloud::

   git push --tags
