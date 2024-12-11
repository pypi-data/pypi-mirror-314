from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
long_description = ""
with open(path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name="autodiscovery",
    packages=["autodiscovery"],
    version="0.0.2",
    license="MIT",
    description="autodiscovery is a Python library that simplifies the discovery of Python applications on a network, allowing seamless connection and interaction between services with minimal configuration.",
    long_description=long_description,
    long_description_content_type= "text/markdown",
    author="Michael Jalloh",
    author_email="michaeljalloh19@gmail.com",
    url="https://github.com/Michael-Jalloh/Autodiscovery",
    package_dir={"autodiscovery":"src/autodiscovery"},
    classifiers= [
        "Development Status :: 4 - Beta",      
        "Intended Audience :: Developers",      
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    platforms=["any"],
    project_urls={
        "issues": "https://github.com/Michael-Jalloh/Autodiscovery/issues",
        "source": "https://github.com/Michael-Jalloh/Autodiscovery"
    },
)