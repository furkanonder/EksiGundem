#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

from setuptools import setup

CURRENT_DIR = Path(__file__).parent


def get_long_description():
    readme_md = CURRENT_DIR / "README.md"
    with open(readme_md, encoding="utf8") as ld_file:
        return ld_file.read()


setup(
    name="eksi",
    version="0.0.1",
    description="Komut satırında Ekşisözlük!",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords=["ekşisözlük", "ekşi", "sözlük"],
    author="Furkan Önder",
    author_email="furkanonder@protonmail.com",
    url="https://github.com/furkanonder/EksiGundem/",
    license="MIT",
    python_requires=">=3.0.0",
    py_modules=["eksi"],
    packages=[],
    zip_safe=False,
    include_package_data=True,
    install_requires=["beautifulsoup4", "bs4", "colorama", "lxml"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={"console_scripts": ["eksi=eksi:eksi"]},
)
