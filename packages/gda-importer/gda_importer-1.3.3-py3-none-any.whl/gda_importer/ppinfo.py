#!/bin/env python3

r"""A simple script for reading pyproject.toml for in CI/CD, tests, etc.

This standalone script is Geometric Data Analytics (c) 2024, available under AGPLv3,
regardless of the other contents of the package it was included with.
"""

import argparse
import logging
import sys

import toml


def main():
    """Run CLI."""
    parser = argparse.ArgumentParser(
        description="Most of this is DEPRECATED BY uv! Try the --extra option on uv install."
    )
    parser.add_argument(
        "-t",
        "--toml",
        type=str,
        default="pyproject.toml",
        help="Path to pyproject.toml TOML file.",
    )

    out_group = parser.add_mutually_exclusive_group(required=True)
    out_group.add_argument(
        "-d",
        "--deps",
        nargs="*",
        help="List the dependencies of the given types.\
                            Available types shown by --listdeps",
    )

    out_group.add_argument(
        "-D",
        "--onlydep",
        nargs="*",
        help="List only the dependency of the given type. "
        "Doesn't include package or build dependencies.",
    )

    out_group.add_argument(
        "-b", "--build", action="store_true", help="List the build dependencies."
    )

    out_group.add_argument(
        "-l",
        "--listdeps",
        action="store_true",
        help="List the options available for --deps",
    )

    out_group.add_argument(
        "-n", "--name", action="store_true", help="Show the package name"
    )

    out_group.add_argument(
        "-v", "--version", action="store_true", help="Show the package version"
    )

    out_group.add_argument(
        "-N",
        "--nameversion",
        action="store_true",
        help="Show name==version for pip specifications",
    )

    args = parser.parse_args()

    # This throws annoying warnings. Suppress them
    logging.captureWarnings(True)
    log = logging.getLogger()
    log.setLevel(logging.ERROR)
    toml_dict = toml.load(args.toml)

    list_deps = toml_dict["project"]["optional-dependencies"].keys()

    if args.listdeps:
        print(" ".join(list_deps))
        sys.exit(0)

    if args.onlydep is not None:
        out_deps = []
        for t in args.onlydep:
            try:
                out_deps.extend(toml_dict["project"]["optional-dependencies"][t])
            except KeyError:
                print(
                    f"Invalid option {t}. "
                    "Use --listdeps to see the valid dependency types."
                )
                sys.exit(1)
        print(" ".join(out_deps))
        sys.exit(0)

    if args.deps is not None:
        out_deps = toml_dict["project"]["dependencies"]
        for t in args.deps:
            try:
                out_deps.extend(toml_dict["project"]["optional-dependencies"][t])
            except KeyError:
                print(
                    f"Invalid option {t}. "
                    "Use --listdeps to see the valid dependency types."
                )
                sys.exit(1)
        print(" ".join(out_deps))
        sys.exit(0)

    if args.build:
        out_deps = toml_dict["build-system"]["requires"]
        print(" ".join(out_deps))
        sys.exit(0)

    if args.name:
        print(toml_dict["project"]["name"])
        sys.exit(0)

    if args.version:
        print(toml_dict["project"]["version"])
        sys.exit(0)

    if args.nameversion:
        a = toml_dict["project"]["name"] + "==" + toml_dict["project"]["version"]
        print(a)
        sys.exit(0)


if __name__ == "__main__":
    main()
