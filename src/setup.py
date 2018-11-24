#!/usr/bin/env python

import setuptools

setuptools.setup(
    name="emonalerts",
    version="0.0.1",
    author="Victoria Fantasy",
    author_email="me@vika.space",
    description="A small package for monitoring your services via email alerts",
    url="https://github.com/kewtree1408",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)