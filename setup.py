#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-05
# @Filename: setup.py
# @Last modified by:   archer
# @Last modified time: 2020-04-08T14:39:26+01:00
# @License: Please see LICENSE file in project root

import os
import subprocess
from setuptools import setup, find_packages, find_namespace_packages

import pathlib


def get_gitVersion():
    """Get the version from git describe in archlinux format."""
    try:
        # getting version from git as this is vcs
        # below equivelant or achlinux versioning scheme:
        # git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g
        git_describe = subprocess.Popen(
            ["git", "describe", "--long"],
            stdout=subprocess.PIPE)
        version_num = subprocess.check_output(
            ["sed", r"s/\([^-]*-\)g/r\1/;s/-/./g"],
            stdin=git_describe.stdout)
        git_describe.wait()
        version_git = version_num.decode("ascii").strip()

    except subprocess.CalledProcessError:
        # for those who do not have git or sed availiable (probably non-linux)
        # this is tricky to handle, lots of suggestions exist but none that
        # neither require additional library or subprocessess
        version_git = "0.0.1"  # for now we will provide a number for you
    return version_git


version = get_gitVersion()
print("version: ", version)

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.rst", "r") as fh:
    readme = fh.read()

namespace_packages = find_namespace_packages(exclude=("docs", "docs.*"))
print("namespace packages:", namespace_packages)

setup(
    name="python-ezdb",
    version=str(version),
    description="Template repository.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="George Onoufriou",
    url="https://github.com/DreamingRaven/python-ezdb",
    packages=namespace_packages,
    scripts=[],
    install_requires=requirements
)
