divio/base
==========

Base images for Python projects deployed on Divio Cloud.


Locally build an image
----------------------

To locally build an image, run the following command::

   ./build.py --repo divio/base --tag 0.00-py3.6-alpine3.7 build

Check `./build.py --help` for additional information.


Test all images
---------------

You can build and test all images locally by running::

   ls -d py* | xargs -I '{}' ./build.py --repo divio/base --target=prod --tag test-{} build
   ls -d py* | xargs -I '{}' ./build.py --repo divio/base --target=dev --tag test-{} build
   ls -d py* | xargs -I '{}' ./build.py --repo divio/base --tag test-{} test


Release process
---------------

Tag commits with the desired Docker image tag, in the form::

   git tag <version>-<flavour>

For your convenience, the `release.py` script can be used to streamline the
tagging operations::

   ./release.py versions --next=minor py*

The command outputs the new tags which would be applied to the repository. Once
asserted the result is correct, re-run the command with the `--tag` flag::

   ./release.py versions --next=minor --tag py*

Then push the tags to GitHub to trigger an automatic build on Docker
Cloud::

   git push --tags github

Please note that GitHub will not trigger webhooks when pushing more than 2 tags
at the same time. When more than two images are updated, push using::

   ./release.py versions --push=github --last py*


Adding a new base image
-----------------------

Add a directory at the root containing an appropriate `Dockerfile``. The image
will be tagged as `divio/base:<version>-<directory-name>`.
