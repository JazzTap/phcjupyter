#!/usr/bin/env python3
from __future__ import print_function

# FIXME: forked from Jupyter code under Modified BSD License

import os
from setuptools import setup

pjoin = os.path.join

here = os.path.abspath(os.path.dirname(__file__))
is_repo = os.path.exists(pjoin(here, '.git'))

''' # from just after version check
packages = []
for d, _, _ in os.walk('jupyterhub'):
    if os.path.exists(pjoin(d, '__init__.py')):
        packages.append(d.replace(os.path.sep, '.'))
'''

setup_args = dict(
    name                = 'phcjupyter',
    version             = '0.1',
    description         = 'support for phcpack jupyterhub deployment',
    author              = 'phcpack team',
    # packages            = ['phcjupyter',],
)

if __name__ == '__main__':
    setup(**setup_args)
