"""
A setuptools-based setup module for the Cryptorix package.
For more details, see:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
"""
# -*- encoding: utf-8 -*-
from __future__ import absolute_import, print_function

import setuptools

# Keywords to improve package discoverability on PyPI
keywords = [
    ""
]

# Reading long description from README.md
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name="sound-fuzz",
    version="1.0.0",
    author="Narendrakumar G S, M V Pranav",
    author_email="narensubbu1@gmail.com, pranavmvp@gmail.com",
    description=(
        ""
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=keywords,
    install_requires=[
        "fuzzywuzzy",
        "py4Soundex",
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.8",  # Specify a minimum Python version
    project_urls={  # Additional URLs for the project
        "Documentation": "https://github.com/Naren210/sound-fuzz#readme",
        "Source": "https://github.com/Naren210/sound-fuzz",
        "Tracker": "https://github.com/Naren210/sound-fuzz/issues"
    },
)
