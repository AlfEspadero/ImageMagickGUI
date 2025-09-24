#!/usr/bin/env python3
"""
Setup script for ImageMagick GUI
"""

from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="imagemagick-gui",
    version="1.0.0",
    author="Alfonso Espadero",
    author_email="contact-imagemagickGUI@alias.alfelfriki.tech",
    description="A simple GUI application for ImageMagick image conversion",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlfEspadero/ImageMagickGUI",
    py_modules=["main"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Topic :: Desktop Environment",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "imagemagick-gui=main:main",
        ],
    },
)