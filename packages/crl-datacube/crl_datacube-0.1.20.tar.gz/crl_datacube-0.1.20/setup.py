from setuptools import setup, find_packages
import os


def parse_requirements(filename):
    with open(filename, "r") as file:
        return [
            line.strip() for line in file if line.strip() and not line.startswith("#")
        ]


requirements_file = os.environ.get("REQUIREMENTS_FILE", "requirements-freeze.txt")
version = os.environ.get("VERSION", "0.1.20")

setup(
    name="crl_datacube",
    version=version,
    packages=find_packages(),
    include_package_data=True,
    package_data={"": ["**/*.csv"]},
    install_requires=parse_requirements(requirements_file),
    author="Chris Lowrie",
    author_email="chlowrie@ucsc.edu",
    description="Utilities for scaling geospatial analyses",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://git.ucsc.edu/chlowrie/datacube",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
