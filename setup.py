#!/usr/bin/env python

from distutils.core import setup

from setuptools import find_packages

setup(name='trdone',
      version='1.0',
      description='Transmission Done Processor',
      author='Miguel Ferreira',
      author_email='miguelferreira@me.com',
      packages=find_packages(),
      license='LICENSE.txt',
      install_requires=[
          'unrar', 'simplejson'
      ]
      )
