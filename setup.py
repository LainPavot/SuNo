#!/usr/bin/env python3

import os

from ticu import __version__
from setuptools import setup, find_packages

current_dir = os.path.dirname(__file__)
LONG_DESC = open(os.path.join(current_dir, "README.md")).read()

with open(os.path.join(current_dir, "requirements.txt")) as f:
  requirements = f.read().splitlines()

setup(
  name=u"ticu",
  version=__version__,
  description="The discord bot for the Tipoui community",
  long_description=LONG_DESC,
  author="Lain Pavot",
  author_email="lain.pavot@protonmail.com",
  license="GNU GENERAL PUBLIC LICENSE v2",
  url="",
  zip_safe=False,
  install_requires=requirements,
  classifiers=[
    "Development Status :: 2.0.0",
    "Intended Audience :: Tipoui Community",
    "Natural Language :: Franch",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
  ],
  packages=find_packages(),
  package_dir={"ticu": "ticu"},
  include_package_data=True,
  entry_points={
    "console_scripts": [
      "ticu = ticu.cli:cli"
    ]
  }
)
