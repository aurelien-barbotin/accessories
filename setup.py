#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 12:41:15 2019

@author: aurelien
"""

from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        return f.read()
    
setup(name='accessories',
      version='0.1',
      description='Miscalleneous accessories',
      long_description = readme(),
      url='',
      packages = find_packages(),
      author='Aurelien Barbotin',
      author_email='aurelien.barbotin@dtc.ox.ac.uk',
      package_data = {},
      include_package_data = False,
      license='MIT',
      zip_safe=False)
