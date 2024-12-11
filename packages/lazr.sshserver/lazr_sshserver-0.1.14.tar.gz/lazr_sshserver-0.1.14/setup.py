#!/usr/bin/env python

# Copyright 2009-2015 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.sshserver
#
# lazr.sshserver is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.sshserver is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.sshserver.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import find_packages, setup


# generic helpers primarily for the long_description
def generate(*docname_or_string):
    res = []
    for value in docname_or_string:
        if value.endswith(".txt"):
            f = open(value)
            value = f.read()
            f.close()
        res.append(value)
        if not value.endswith("\n"):
            res.append("")
    return "\n".join(res)


# end generic helpers


setup(
    name="lazr.sshserver",
    version="0.1.14",
    namespace_packages=["lazr"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    maintainer="LAZR Developers",
    maintainer_email="lazr-developers@lists.launchpad.net",
    description=open("README.txt").readline().strip(),
    long_description=generate("src/lazr/sshserver/README.txt", "NEWS.txt"),
    license="LGPL v3",
    install_requires=[
        "setuptools",
        "Twisted[conch]>=16.2.0",
        "zope.component",
        "zope.event",
        "zope.interface",
    ],
    url="https://launchpad.net/lazr.sshserver",
    project_urls={
        "Source": "https://code.launchpad.net/lazr.sshserver",
        "Issue Tracker": "https://bugs.launchpad.net/lazr.sshserver",
    },
    download_url="https://launchpad.net/lazr.sshserver/+download",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",  # noqa: E501
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
    extras_require=dict(
        docs=["Sphinx"],
        test=[
            "breezy",
            "fixtures",
            "flake8",
            "testtools",
            "zope.testrunner",
        ],
    ),
    python_requires=">=3.8",
    test_suite="lazr.sshserver.tests",
)
