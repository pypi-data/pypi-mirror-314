import sys
from setuptools import setup, Extension, find_packages
from os import environ
import os

extra_compile_args = []
extra_link_args = []
if 'darwin' in sys.platform:
    target_dirs = ["gcc-9", "gcc-10", "gcc-11", "gcc-12", "gcc-13", "gcc-14", "gcc-15"]
    path = "/opt/homebrew/bin/"
    directories = [dir for dir in os.listdir(path) if dir in target_dirs]
    if len(directories) > 0:
        gcc_version = directories[0]
        if 'gcc-9' == gcc_version:
            gcc_path = "/opt/homebrew/bin/gcc-9"
        elif 'gcc-10' == gcc_version:
            gcc_path = "/opt/homebrew/bin/gcc-10"
        elif 'gcc-11' == gcc_version:
            gcc_path = "/opt/homebrew/bin/gcc-11"
        elif 'gcc-12' == gcc_version:
            gcc_path = "/opt/homebrew/bin/gcc-12"
        elif 'gcc-13' == gcc_version:
            gcc_path = "/opt/homebrew/bin/gcc-13"
        elif 'gcc-14' == gcc_version:
            gcc_path = "/opt/homebrew/bin/gcc-14"
        else:
            gcc_path = ""
        extra_compile_args = ['-fopenmp']
        extra_link_args = ['-fopenmp']
        os.environ["CC"] = gcc_path
else:
    if environ.get('CC') and 'clang' in environ['CC']:
        # clang
        extra_compile_args = ['-fopenmp=libomp']
        extra_link_args = ['-fopenmp=libomp']
    else:
        # GNU
        extra_compile_args = ['-fopenmp']
        extra_link_args = ['-fopenmp']
MOD1 = 'kssdtool'
sources1 = ['co2mco.c',
            'iseq2comem.c',
            'command_dist_wrapper.c',
            'mytime.c',
            'global_basic.c',
            'command_set.c',
            'command_dist.c',
            'command_shuffle.c',
            'command_composite.c',
            'mman.c',
            'pykssd.c']
include_dirs1 = ['kssdheaders']

setup(
    name='kssdutils',
    version='1.0.5',
    author='Hang Yang',
    author_email='yhlink1207@gmail.com',
    description="kssdutils is a Python package for genome analysis, such as sketch, dist.",
    ext_modules=[
        Extension(MOD1, sources=sources1, include_dirs=include_dirs1, libraries=['z'],
                  extra_compile_args=extra_compile_args,
                  extra_link_args=extra_link_args)
    ],
    py_modules=['kssdutils'],
    packages=find_packages(),
    dependency_links=['https://pypi.python.org/simple/'],
    zip_safe=False,
    include_package_data=True
)

