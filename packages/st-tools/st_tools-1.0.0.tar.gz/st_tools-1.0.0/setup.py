# -*- coding: utf-8 -*-
"""
st_tools setup
"""

import io
import os

import setuptools

HERE = os.path.abspath(os.path.dirname(__file__))


def get_version(file, name="__version__"):
    """
    Get the version of the package from the given file by
    executing it and extracting the given `name`.
    """
    path = os.path.realpath(file)
    version_ns = {}
    with io.open(path, encoding="utf8") as f:
        exec(f.read(), {}, version_ns)
    return version_ns[name]


__version__ = get_version(os.path.join(HERE, "st_tools/_version.py"))

with io.open(os.path.join(HERE, "README.md"), encoding="utf8") as fh:
    long_description = fh.read()

setup_args = dict(
    name="st_tools",
    version=__version__,
    url="https://github.com/dsblank/st_tools",
    author="st_tools Development Team",
    description="Tools for streamlit",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[
        "st_tools",
    ],
    python_requires=">=3.7",
    license="MIT License",
    platforms="Linux, Mac OS X, Windows",
    keywords=["streamlit"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)

if __name__ == "__main__":
    setuptools.setup(**setup_args)
