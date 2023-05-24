#! /usr/bin/env python3
# This script uses only the standardlib because that is what
# is available on in the context of the CI/CD platform.
import os
import argparse


def get_image_name(repo, tag, target):
    if target == "prod":
        return "{}:{}".format(repo, tag)
    else:
        return "{}:{}-{}".format(repo, tag, target)


def parse_image_name(image_name):
    repo, tag = image_name.rsplit(":", 1)
    if tag.endswith("-dev"):
        tag = tag[:-4]
        target = "dev"
    else:
        target = "prod"
    return repo, tag, target


def get_context_path_from_tag(tag):
    version, directory = tag.split("-", 1)
    if directory.endswith("-dev"):
        directory = directory[:-4]
    return directory


def get_build_command(repo, tag, target):
    return [
        "docker",
        "build",
        "-t",
        get_image_name(repo, tag, target),
        "--build-arg",
        "TARGET={}".format(target),
        "--no-cache",
        get_context_path_from_tag(tag=tag),
    ]


def get_test_command(repo, tag, target):
    """
    Builds and returns a command to test the resulting image.

    The tests execute the following operations:

    * `pip-reqs` `compile` and `resolve` on an arbitrary platform (it's not an
       issue if the platform does not match the platform of the image, as the
       resulting requirements.urls file will never be used);
    * `pip install` a series of packages known to stress the build phase (we
       force them to be build from source).

    Note that the `pip-reqs` and the `pip install` steps are completely
    independent on purpose (the installation step does not use the resolved
    requirements from `pip-reqs`). We are just smoke testing `pip-reqs` on the
    first step, and making sure that we are able to use the dev image to build
    binary wheels in the second step.
    """
    with open(".artifacts/test/requirements.in", "w") as fh:
        fh.write("django\n")

    packages = [
        "psycopg2",
        "cryptography",
        "pybind11",
        "numpy",
        "scipy",
        "pillow",
        "lxml",
        "pyyaml",
        "easy_thumbnails[svg]",
    ]
    accept_wheels = [
        "importlib-metadata",
        "zipp",
        "freetype-py",
    ]
    pip_command = "pip install --no-binary :all: --only-binary {} {}".format(
        ",".join(accept_wheels),
        " ".join(packages),
    )
    return [
        "docker",
        "run",
        "-v"
        "{}/.artifacts/test:/app:rw".format(
            os.path.abspath(os.path.dirname(__file__))
        ),
        "-e",
        "WHEELSPROXY_URL=https://wheels.aldryn.net/v1/pypi/buster-py39/",
        "-e",
        "NPY_NUM_BUILD_JOBS={}".format(os.cpu_count()),
        get_image_name(repo, tag, target),
        "sh",
        "-c",
        "pip-reqs compile && pip-reqs resolve && {}".format(pip_command),
    ]


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("operation", help='The operation: "build" or "test"')
    parser.add_argument(
        "--repo",
        default=os.environ.get("DOCKER_REPO", "divio/base"),
        help="The repository name",
    )
    parser.add_argument(
        "--tag",
        default=os.environ.get("DOCKER_TAG", ""),
        help='A tag name like "4.42-py3.6-alpine". Do not include the "-dev" '
        "suffix, instead set the --target option.",
    )
    parser.add_argument(
        "--target",
        default=os.environ.get("TARGET", "prod"),
        help="The build target (dev or prod).",
    )

    args = parser.parse_args()

    operation = args.operation

    image_name = os.environ.get("IMAGE_NAME")
    if image_name:
        # When dockerhub builds IMAGE_NAME will be set and will override any
        # other options.
        repo, tag, target = parse_image_name(image_name=image_name)
    else:
        # For local building we can use these env vars.
        repo = str(args.repo)
        tag = str(args.tag)
        target = str(args.target)
    if not (repo and tag and target):
        print("Missing parameters!")
        exit(code=1)
    if tag.endswith("-dev"):
        print(
            "Do not include the -dev suffix in the tag. "
            "Set `--target` instead."
        )
        exit(code=1)

    if operation == "build":
        command = get_build_command(
            repo=repo, tag=tag, target=target
        )
    elif operation == "test":
        command = get_test_command(repo=repo, tag=tag, target=target)

    print("repo: {}".format(repo))
    print("tag: {}".format(tag))
    print("target: {}".format(target))
    print("command:")
    print(" ".join(command))
    os.execvp(command[0], command)


if __name__ == "__main__":
    main()
