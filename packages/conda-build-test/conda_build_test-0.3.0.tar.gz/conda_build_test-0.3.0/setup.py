import os
from setuptools import setup, Extension

EXT_MODULES = [
    # Extension(
    #     'hello.hello',
    #     sources=[os.path.join('src', 'hello.c')],
    # )
]

setup(ext_modules=EXT_MODULES)
