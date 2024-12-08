# setup.py
from distutils.core import setup, Extension
from Cython.Build import cythonize
# import xarray
import numpy

setup(name='cython_extend',
ext_modules = cythonize(Extension(
    name='cython_extend',
    sources=['cython_extend.pyx'],
    language='c',
    include_dirs=[numpy.get_include()],
    library_dirs=[],
    libraries=[],
    extra_compile_args=[],
    extra_link_args=[]
)))