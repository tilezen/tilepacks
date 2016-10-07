# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='tilepack',
    version='1.0.0',
    description='Save tiles in a package',
    long_description=readme,
    author='Ian Dees',
    author_email='ian.dees@mapzen.com',
    url='https://github.com/tilezen/tilepacks',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': ['tilepack=tilepack.builder:main'],
    }
)
