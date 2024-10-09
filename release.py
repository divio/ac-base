#! /usr/bin/env python
# This script uses only the standardlib because to make it portable
# and usable from any context (e.g. CI/CD)
import argparse
import os
import subprocess
import sys

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
            print(f"Flavor not found: {flavor}")
            sys.exit(-1)

        if args.last:
            version = versions[-1]
            tag = f"{version}-{flavor}"
            print(tag)
            if args.push:
                remote = args.push
                print(f"Pushing tag {tag} to {remote}")
                subprocess.check_call(["git", "push", remote, tag])
        elif args.next:
            if versions:
                version = versions[-1]
                major, minor, _patch = (
                    version.major,
                    version.minor,
                    version.micro,
                )
                _patch = 0
                if args.next == "minor":
                    minor += 1
                elif args.next == "major":
                    major += 1
                    minor = 0
                version = Version(f"{major}.{minor}")
            else:
                version = Version("1.0")

            tag = f"{version}-{flavor}"
            if args.tag:
                print(f"{flavor} => created tag for {version}:\n  {tag}")
                subprocess.check_call(["git", "tag", tag])
            else:
                print(tag)
        else:
            print(flavor)
            for version in reversed(versions):
                print(version)


def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    subparsers = parser.add_subparsers()
    parser_versions = subparsers.add_parser(
        "versions",
        help="Manage versions: either print existing ones, or bump and tag the next one",
    )
    parser_versions.add_argument(
        "--last",
        action="store_true",
        help="Print the last version(s) without bumping anything",
    )
    parser_versions.add_argument(
        "--next",
        choices=["major", "minor", "test"],
        default=None,
        help="Bump to the next version",
    )
    parser_versions.add_argument(
        "--tag",
        action="store_true",
        help="Create the git tags (requires --next)",
    )
    parser_versions.add_argument(
        "--push",
        help="Push the last tag to the given remote (requires --last), e.g. origin",
    )
    parser_versions.add_argument(
        "flavors", nargs="+", help="Pattern(s) to consider, e.g. py3*"
    )
    parser_versions.set_defaults(func=versions)

    args = parser.parse_args()
    if (args.last or args.push) and (args.next or args.tag):
        parser.error("Cannot use --last/--push with --next/--tag")

    if args.tag and not args.next:
        parser.error("Must use --next with --tag")

    if args.push and not args.last:
        parser.error("Must use --last with --push")

    args.func(args)


if __name__ == "__main__":
    main()
