#! /usr/bin/env python
# This script uses only the standardlib because that is what
# is available on in the context of the CI/CD pipeline.
import os
import sys
import argparse
import subprocess
from packaging.version import Version, parse


def get_tags(suffix=None):
    tags = subprocess.check_output(["git", "tag"]).decode("utf-8")
    tags = [t.strip() for t in tags.splitlines()]
    if suffix:
        tags = [t for t in tags if t.endswith(suffix)]
    return tags


def extract_versions(tags):
    return sorted(parse(t.split("-", 1)[0]) for t in tags)


def versions(args):
    for flavor in sorted(args.flavors):
        tags = get_tags(flavor)
        versions = extract_versions(tags)

        if not versions and not os.path.exists(flavor):
            print("Flavor not found: {}".format(flavor))
            sys.exit(-1)

        if args.last:
            version = versions[-1]
            tag = "{}-{}".format(version, flavor)
            print(tag)
            if args.push:
                remote = args.push
                print("Pushing tag {} to {}".format(tag, remote))
                subprocess.check_call(["git", "push", remote, tag])
        elif args.next:
            print(flavor)
            if versions:
                version = versions[-1]
                major, minor, patch = version.major, version.minor, version.micro
                patch = 0
                if args.next == "minor":
                    minor += 1
                elif args.next == "major":
                    major += 1
                    minor = 0
                version = Version(f"{major}.{minor}")
            else:
                version = Version("1.0")
            if args.tag:
                tag = "{}-{}".format(version, flavor)
                print(
                    "Tagging repo with tag {} for version {}".format(
                        tag, version
                    )
                )
                subprocess.check_call(["git", "tag", tag])
            else:
                print(version)
        else:
            print(flavor)
            for version in reversed(versions):
                print(version)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()
    parser_versions = subparsers.add_parser("versions")
    parser_versions.add_argument("--last", action="store_true")
    parser_versions.add_argument("--next", nargs="?", const="minor")
    parser_versions.add_argument("--tag", action="store_true")
    parser_versions.add_argument("--push")
    parser_versions.add_argument("flavors", nargs="+")
    parser_versions.set_defaults(func=versions)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
