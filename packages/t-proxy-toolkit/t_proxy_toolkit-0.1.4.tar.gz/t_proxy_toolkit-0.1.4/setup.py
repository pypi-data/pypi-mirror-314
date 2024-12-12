#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.md") as readme_file:
    readme = readme_file.read()

install_requirements = open("requirements.txt").readlines()

setup(
    author="Thoughtful",
    author_email="support@thoughtful.ai",
    python_requires=">=3.9",
    classifiers=[
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
    ],
    description="Wrapper around selenium and requests to make it easier to use proxies.",
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords="t-proxy-toolkit",
    name="t-proxy-toolkit",
    packages=find_packages(include=["t_proxy", "t_proxy.*"]),
    test_suite="tests",
    url="https://www.thoughtful.ai/",
    version="0.1.4",
    zip_safe=False,
    install_requires=install_requirements,
    include_package_data=True,
)
