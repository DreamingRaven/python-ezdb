#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-05
# @Filename: setup.py
# @Last modified by:   archer
# @Last modified time: 2020-04-08T14:39:26+01:00
# @License: Please see LICENSE file in project root

import subprocess
from setuptools import setup, find_packages, find_namespace_packages


# getting version from git as this is vcs
# below equivelant: git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g
git_describe = subprocess.Popen(["git", "describe", "--long"],
                                stdout=subprocess.PIPE)
version_num = subprocess.check_output(["sed", r"s/\([^-]*-\)g/r\1/;s/-/./g"],
                                      stdin=git_describe.stdout)
git_describe.wait()
version_git = version_num.decode("ascii").strip()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.rst", "r") as fh:
    readme = fh.read()

namespace_packages = find_namespace_packages(exclude="docs.*")
print("namespace packages:", namespace_packages)

setup(
    name="python-ezdb",
    version=str(version_git),
    description="Template repository.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="George Onoufriou",
    url="https://github.com/DreamingRaven/python-ezdb",
    packages=namespace_packages,
    scripts=[],
    install_requires=requirements
)
