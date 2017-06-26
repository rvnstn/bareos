#!/usr/bin/python

from setuptools import find_packages, setup

setup(
    name='bareos-fuse',
    version='0.2',
    author='Joerg Steffens',
    author_email='joerg.steffens@bareos.com',
    #packages=find_packages(),
    package_dir = { 
        'bareos.fuse': 'bareos/fuse',
        'bareos.fuse.node': 'bareos/fuse/node',
    },
    packages=['bareos.fuse', 'bareos.fuse.node'],
    scripts=['bin/bareos-fuse.py'],
    url='https://github.com/bareos/bareos-fuse/',
    # What does your project relate to?
    keywords='bareos fuse filesystem',
    description='Virtual Filesystem Showing Bareos Information.',
    long_description=open('README.rst').read(),
    install_requires=[
        'python-bareos',
        'python-fuse'
    ]
)
