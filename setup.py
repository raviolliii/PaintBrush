from distutils.core import setup
from Cython.Build import cythonize

paint_brush = cythonize('Brush.pyx')
setup(ext_modules=paint_brush)
