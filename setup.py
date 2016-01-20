#!/usr/bin/env python
"""Project setup."""
import os
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

# Requirements specified up to the minor version to allow bugfixes to be automatically applied.
REQUIREMENTS = [
]

# Versions of test requirements kept exact to avoid broken builds due to API breakage in updates.
TEST_REQUIREMENTS = [
    'pylama==7.0.6',
    'pytest==2.8.5',
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
        'Programming Language :: Python :: 2.7',
    ],
    keywords='pytest order reorder test',
    author='Michał Pawłowski',
    author_email='@'.join(['unittestablecode', 'gmail.com']),
    license='MIT',
    packages=find_packages(exclude=['test']),
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    extras_require={'tests': TEST_REQUIREMENTS},
    cmdclass={},
    entry_points={
    },
)
