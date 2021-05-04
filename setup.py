# -*- coding: utf-8 -*-
"""
Created on Tue Jan 21 10:37:05 2020

@author: aweis
"""
from setuptools import setup,find_packages

setup(name='pyfolio',
      version='0.1',
      description='Library for desigining and testing financial portfolios.',
      author='Alec Weiss',
      author_email='alec@weissworks.dev',
      url='https://www.weissworks.dev',
      packages=find_packages(),
     )


#build with `pip install -e .`