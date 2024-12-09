#!/usr/bin/env python

"""
Licensed under BSD license
"""

from setuptools import setup, find_packages

setup(name='bflb-crypto-plus',
      version='1.1',
      description='PyCrypto Cipher extension',
      author='Christophe Oosterlynck',
      author_email='tiftof@gmail.com',
      packages = find_packages('src'),
      install_requires = ['pycryptodome'],
      package_dir={'': 'src'},
      license="BSD",
     )

