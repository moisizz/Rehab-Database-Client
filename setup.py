from distutils.core import setup
import sys
import py2exe

setup(windows=[{"script": "main_module.py",
                "icon_resources": [(1, "logo.ico")]}],
       
      options = { "py2exe":{"dll_excludes":["MSVCP90.dll"], 
                  "includes" : ["sip","sqlite3","sqlalchemy.dialects.sqlite"]}})