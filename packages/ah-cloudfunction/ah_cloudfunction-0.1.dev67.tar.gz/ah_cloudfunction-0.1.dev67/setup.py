"""
Setup script for thdp-hds-cloud-functions.

This script uses setuptools_scm to dynamically determine the version
of the package based on the version control tags.
"""
import sys
from setuptools import setup

sys.path.insert(0, "thdp-hds-cloud-functions")

setup(
    use_scm_version={
        "write_to": "version.txt",
        "tag_regex" : "^release-v(?P<version>\\d+\\.\\d+\\.\\d+)$",
        "local_scheme" : "no-local-version"
    },
    setup_requires=["setuptools_scm"],
)

