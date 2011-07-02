"""
Script for building the sigil window.

Adapted from:

http://www.rkblog.rk.edu.pl/w/p/building-mac-os-x-applications-py2app/

Usage:
    python setup.py py2app
"""
from setuptools import setup


OPTIONS = {'includes': ['sip']}


setup(
    app = ["sigils.py"],
    options = { 'py2app': OPTIONS },
    setup_requires = ["py2app"],
)
