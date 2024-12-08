# -*- coding: utf-8 -*-
import codecs
import os
import re
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

setup(
    name='goodhomepy',
    version=find_version("goodhomepy", "__init__.py"),
    packages=find_packages(),
    url='https://github.com/biker91620/goodhomepy',
    license='',
    author='biker91620',
    author_email='biker91620@gmail.com',
    description='Good Home API Client is a Python client for interacting with the Good Home API. This client allows you to manage authentication, refresh tokens, verify tokens, and retrieve information about users, devices, and homes via the Good Home API.',
    long_description_content_type='text/markdown',
    long_description=read("README.md"),
)
