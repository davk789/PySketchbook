"""
    py2exe build script
"""

from py2exe.build_exe import py2exe
from distutils.core import setup

P2EOPTIONS = {"includes":["sip"]}

setup(windows = ["sigils.py"],
      options = {"py2exe": P2EOPTIONS }) 

