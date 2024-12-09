"""Setup for the validate_version_code package."""

import os
import re

# To use a consistent encoding
from codecs import open as copen
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with copen(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


def read(*parts):
    """Build an absolute path from *parts and and return the contents of the resulting file."""
    with copen(os.path.join(here, *parts), "r", encoding="utf-8") as fp:
        return fp.read()


def find_version(*file_paths):
    """Find the version number in the file at *file_paths."""
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


__version__ = find_version("validate_version_code", "__version__.py")

test_deps = ["pytest", "pytest-cov", "pytest-readme"]

extras = {
    "test": test_deps,
}

setup(
    name="validate_version_code",
    version=__version__,
    description="Python package to validate version codes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LucaCappelletti94/validate_version_code",
    author="Luca Cappelletti",
    author_email="cappelletti.luca94@gmail.com",
    # Choose your license
    license="MIT",
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(exclude=["contrib", "docs", "tests*"]),
    tests_require=test_deps,
    extras_require=extras,
)
