#!/usr/bin/env python
#
# Copywright (C) 2024 Debmalya Pramanik <neuralNOD@gmail.com>
# LICENSE: MIT License

from setuptools import setup
# from setuptools import find_packages

import statology as stats

setup(
    name = "statology",
    version = stats.__version__,
    author = "shark-utilities developers",
    author_email = "neuralNOD@outlook.com",
    description = "Collection of Statistical Function",
    # long_description = open("README.md", "r").read(),
    # long_description_content_type = "text/markdown",
    url = "https://github.com/sharkutilities/statology",
    # packages = find_packages(),
    classifiers = [
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License"
    ],
    project_urls = {
        "Issue Tracker" : "https://github.com/sharkutilities/statology/issues",
        # "Code Documentations" : "https://statology.readthedocs.io/en/latest/index.html",
        "Org. Homepage" : "https://github.com/sharkutilities"
    },
    keywords = [
        # keywords for finding the package::
        "numpy", "array", "utility", "utilities", "util", "utils",
        # keywords for finding the package relevant to usecases::
        "wrappers", "data science", "data analysis", "data scientist", "data analyst",
        # keywords as per available functionalities::
        "statistics", "outliers", "percentile", "quantile", "probability"
    ],
    # python_requires = ">=3.9"
)
