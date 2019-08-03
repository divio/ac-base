#! /usr/bin/env python
# This script uses python 2.7.6 and only the standardlib because that is what
# is available on in the context of the build hook on docker cloud / dockerhub.
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
        get_context_path_from_tag(tag=tag),
    ]


def get_test_command(repo, tag, target):
    packages = [
        "psycopg2",
        "cryptography",
        "numpy",
        "scipy",
        "pillow",
        "lxml",
        "pyyaml",
    ]
    return [
        "docker",
        "run",
        "-it",
        get_image_name(repo, tag, target),
        "pip",
        "install",
    ] + packages


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
        command = get_build_command(repo=repo, tag=tag, target=target)
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
