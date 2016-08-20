# from distutils.core import setup
from Cython.Build import cythonize

from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import  build_ext
import numpy as np
# setup(
#     ext_modules = cythonize("solutions.pyx")
# )


setup(
	cmdclass = {'build_ext': build_ext},
	include_dirs = [np.get_include()],
	ext_modules = [Extension("solutions", ["solutions.pyx"] )]
)