#!/usr/bin/env python

from distutils.core import setup

version = '0.01'

packages = ['ctbBio27']

scripts = ['ctbBio27/id2tax.py', 'ctbBio27/kegginfo.py', 'ctbBio27/ssu_tree.py']

classifiers = ['Programming Language :: Python', 'Programming Language :: Python :: 2.7']

requirements = ['tokyocabinet'],

setup(name='ctbBio27',
      author='Chris Brown',
      author_email='ctb@berkeley.edu',
      packages=packages,
      scripts=scripts,
      version=version,
      license='MIT',
      url='https://github.com/christophertbrown/bioscripts27',
      description='some useful scripts for working with genomics and sequencing data that are stuck in the past (python 2.7)',
      install_requires=requirements,
      classifiers=classifiers
      )
