#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name="openeleccreator",
      py_modules=['openeleccreator'],
      packages=['sdcardburner'],
      version="1.0",
      description="OpenELEC SDCard Creator",
      license="MIT",
      author="Andrea Stagi",
      author_email="stagi.andrea@gmail.com",
      url="https://github.com/astagi/openelec-creator",
      keywords= "openelec flash sdcard",
      install_requires=[
        "requests",
      ],
      entry_points = {
        'console_scripts': [
          'openeleccreator = openeleccreator:main',
        ],
      },
      zip_safe = True)
