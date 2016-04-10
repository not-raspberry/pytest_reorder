#!/usr/bin/env python
# coding: utf-8
"""Project setup."""
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

REQUIREMENTS = [
    'pytest',
]

TEST_REQUIREMENTS = [
    'pylama==7.0.6',
    'pytest==2.8.5',
    'mock==1.3.0',
]

setup(
    name='pytest_reorder',
    version='0.0.1',
    description='Reorder tests depending on their names.',
    long_description=README,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing'
        'License :: OSI Approved :: MIT License',
        'Framework :: Pytest',
        # Let's be honest - most development happens under Python 2.7.
        # All other Pythons are build by Travis. It should be enough because the test suite
        # actually tests something.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: POSIX :: Linux',
    ],
    keywords='pytest order reorder test',
    author='Michał Pawłowski',
    author_email='@'.join(['unittestablecode', 'gmail.com']),
    license='MIT',
    packages=find_packages(exclude=['tests']),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require={'tests': TEST_REQUIREMENTS},
    entry_points={
        'pytest11': 'reorder=pytest_reorder.hook'
    }
)
