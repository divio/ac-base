#! /usr/bin/env python
# This script uses python 2.7.6 and only the standardlib because that is what
# is available on in the context of the build hook on docker cloud / dockerhub.
import os
import sys
import argparse
import subprocess
from distutils.version import StrictVersion


def get_tags(suffix=None):
    tags = subprocess.check_output(["git", "tag"]).decode("utf-8")
    tags = [t.strip() for t in tags.splitlines()]
    if suffix:
        tags = [t for t in tags if t.endswith(suffix)]
    return tags


def extract_versions(tags):
    return sorted(StrictVersion(t.split("-", 1)[0]) for t in tags)


def versions(args):
    for flavor in args.flavors:
        print(flavor)
        tags = get_tags(flavor)
        versions = extract_versions(tags)

        if not versions and not os.path.exists(flavor):
            print("Flavor not found: {}".format(flavor))
            sys.exit(-1)

        if args.last:
            print(versions[-1])
        elif args.next:
            if versions:
                version = versions[-1]
                major, minor, patch = version.version
                patch = 0
                if args.next == "minor":
                    minor += 1
                elif args.next == "major":
                    major += 1
                    minor = 0
                version.version = major, minor, patch
            else:
                version = StrictVersion("1.0")
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
    parser_versions.add_argument("flavors", nargs="+")
    parser_versions.set_defaults(func=versions)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
