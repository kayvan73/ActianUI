#!/usr/bin/env python
from distutils.core import setup, Extension
btrievePython_module = Extension('_btrievePython',
    sources=['btrievePython_wrap.cxx'],
    library_dirs=['/usr/local/psql/lib/'],
    runtime_library_dirs=['/usr/local/psql/lib'],
    libraries=['btrieveCpp'] )
setup (name='btrievePython',
    version='1.0',
    author='Actian',
    description="""Compile Btrieve 2 Python module""",
    ext_modules=[btrievePython_module],
    py_modules=["btrievePython"], )

