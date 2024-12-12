#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import find_packages, setup


def parse_requirements():
    path = Path(__file__).parent.resolve() / "requirements.txt"
    assert path.exists(), f"Missing requirements: {path}"
    return list(map(str.strip, path.read_text().splitlines()))


setup(
    name="teklia-line-image-extractor",
    version=open("VERSION").read(),
    description="A tool for extracting a text line image from the contour with different methods",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Martin Maarand",
    author_email="maarand@teklia.com",
    install_requires=parse_requirements(),
    entry_points={
        "console_scripts": ["line-image-extractor=line_image_extractor.main:main"]
    },
    packages=find_packages(),
    include_package_data=True,
    keywords="line transformation image extraction",
    url="https://gitlab.teklia.com/atr/line_image_extractor",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
)
