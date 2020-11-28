# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="ldpy",
    version="0.2.1",
    packages=find_packages(),
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/pabloalarconm/ldpy",
    description="Client-side module for managing Linked data Platform (meta)data.",
    license="MIT",
    keywords="LDP client container resource",
    long_description=readme
)
