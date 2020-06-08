#!/usr/bin/python

from setuptools import find_packages, setup

setup(
    name="bareos-fuse",
    #version="0.3.dev2",
    version="0.3",
    license="AGPLv3",
    author="Joerg Steffens",
    author_email="joerg.steffens@bareos.com",
    #packages=find_packages(),
    package_dir = { 
        "bareos.fuse": "bareos/fuse",
        "bareos.fuse.node": "bareos/fuse/node",
    },
    packages=["bareos.fuse", "bareos.fuse.node"],
    scripts=["bin/bareos-fuse.py"],
    url="https://github.com/bareos/bareos-fuse/",
    keywords="bareos fuse filesystem bareosfs",
    description="Virtual Filesystem showing Bareos information.",
    long_description=open("README.rst").read(),
    long_description_content_type='text/x-rst',
    install_requires=[
        "fuse-python",
        "python-bareos",
        "python-dateutil",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: System :: Archiving :: Backup",
    ],
)
