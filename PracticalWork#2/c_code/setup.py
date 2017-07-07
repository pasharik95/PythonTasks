from distutils.core import setup, Extension

foo_module = Extension('_c_code', sources=['c_code_wrap.c', 'c_code.c'])

setup(name='c_code', ext_modules=[foo_module], py_modules=["c_code"])

