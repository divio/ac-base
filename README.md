# divio/base

Base images for Python projects deployed on Divio Cloud.

## Locally build an image

To locally build an image, run the following command:

```bash
./build.py --repo divio/base --tag 0.00-py3.6-alpine3.7 build
```

To build for a different architecture than your machine\'s one, set the
[DOCKER_DEFAULT_PLATFORM]{.title-ref} environment variable:

```bash
DOCKER_DEFAULT_PLATFORM=linux/arm64 ./build.py --repo divio/base --tag 1.1-py3.11-slim-bullseye build
```

Check `./build.py --help` for additional information.

## Test all images

You can build and test all images locally by running:

```bash
ls -d py* | xargs -I '{}' ./build.py --repo divio/base --target=prod --tag test-{} build
ls -d py* | xargs -I '{}' ./build.py --repo divio/base --target=dev --tag test-{} build
ls -d py* | xargs --open-tty -I '{}' ./build.py --repo divio/base --target=dev --tag test-{} test
```

## Release process

Tag commits with the desired Docker image tag, in the form:

```bash
git tag <version>-<flavour>
```

For your convenience, the `release.py` script can be used to streamline the tagging
operations:

```bash
./release.py versions --next=minor py*
```

The command outputs the new tags which would be applied to the repository. Once asserted the result
is correct, re-run the command with the `--tag` flag:

```bash
./release.py versions --next=minor --tag py*
```

Then push the tags to Gitlab to trigger an automatic build:

```bash
git push --tags origin
```

You can also selectively push only the last tags created for given flavors via the `release.py`
script:

```bash
./release.py versions --last --push=origin py*
```

## Adding a new base image

Add a directory at the root containing an appropriate `Dockerfile`. The image will be
tagged as `divio/base:<version>-<directory-name>`.

## Marking an image as EOL

To mark an image as EOL, just rename its folder by adding the `EOL-` prefix.
