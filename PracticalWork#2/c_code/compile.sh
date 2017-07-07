#! /bin/bash

swig -python c_code.i

python setup.py build_ext --inplace
