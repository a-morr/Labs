from distutils.core import setup
from Cython.Build import cythonize

setup(name="old_solutions", ext_modules=cythonize('old_solutions.pyx'))
