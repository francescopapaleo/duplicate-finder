#!/usr/bin/env python

from pathlib import Path
from setuptools import setup, find_packages

NAME = "duplicate-finder"
DESCRIPTION = "Utility for finding duplicate files."
URL = ""
EMAIL = ""
AUTHOR = "Francesco Papaleo"
REQUIRES_PYTHON = ">=3.6.0"
VERSION = "0.1.0"

HERE = Path(__file__).parent

try:
    with open(HERE / "README.md", encoding="utf-8") as f:
        long_description = "\n" + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=["duplicate_finder"],
    install_requires=["pandas", "tqdm"],
    include_package_data=True,
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
    ],
)
