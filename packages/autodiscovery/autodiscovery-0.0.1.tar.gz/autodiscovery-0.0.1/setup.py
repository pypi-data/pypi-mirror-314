from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
long_description = ""

setup(
    name="autodiscovery",
    packages=["autodiscovery"],
    version="0.0.1",
    license="MIT",
    description="",
    author="Michael Jalloh",
    author_email="michaeljalloh19@gmail.com",
    package_dir={"autodiscovery":"src/autodiscovery"}
)