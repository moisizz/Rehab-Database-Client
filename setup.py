from distutils.core import setup
import sys
import py2exe

setup(windows=['main_module.py'], options = { "py2exe":{"dll_excludes":["MSVCP90.dll"], "includes" : ["sip","sqlite3","sqlalchemy.dialects.sqlite"]}})