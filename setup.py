#!/usr/bin/env python

import re
from setuptools import setup, find_packages

pkgname = 'datastore.objects'

# gather the package information
main_py = open('datastore/objects/__init__.py').read()
metadata = dict(re.findall("__([a-z]+)__ = '([^']+)'", main_py))
packages = filter(lambda p: p.startswith('datastore'), find_packages())

# convert the readme to pypi compatible rst
try:
  try:
    import pypandoc
    readme = pypandoc.convert('README.md', 'rst')
  except ImportError:
    readme = open('README.md').read()
except:
  print 'something went wrong reading the README.md file.'
  readme = ''

setup(
  name=pkgname,
  version=metadata['version'],
  description='object mapper for datastore',
  long_description=readme,
  author=metadata['author'],
  author_email=metadata['email'],
  url='http://github.com/datastore/datastore.objects',
  keywords=[
    'datastore',
    'object mapper',
    'ORM',
    'serializing'
  ],
  license='MIT License',
  packages=packages,
  namespace_packages=['datastore'],
  install_requires=['datastore>=0.3.4'],
  test_suite='datastore.objects.test',
  classifiers=[
    'Topic :: Database',
  ]
)
