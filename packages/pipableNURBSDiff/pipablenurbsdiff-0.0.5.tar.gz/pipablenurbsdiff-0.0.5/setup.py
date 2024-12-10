from setuptools import setup, find_packages
import torch
from torch.utils.cpp_extension import CppExtension, CUDAExtension
import os


class BuildExtension(torch.utils.cpp_extension.BuildExtension):
    def __init__(self, *args, **kwargs):
        super().__init__(use_ninja=False, *args, **kwargs)


os.environ["TORCH_CUDA_ARCH_LIST"] = '5.0;5.2;5.3;6.0;6.1;6.2;7.0;7.2;7.5;8.0;8.6;8.7;8.9;9.0'

this_dir = os.path.dirname(os.path.abspath(__file__))
extensions_dir = os.path.join(this_dir, "NURBSDiff", "csrc")
extra_compile_args = {"cxx": ["-std=c++17"]}
include_package = ('NURBSDiff*', 'NURBSDiff/csrc')
try:
    setup(
        ext_modules=[
            CppExtension(name='NURBSDiff.curve_eval_cpp',
                         sources=['NURBSDiff/csrc/curve_eval.cpp', 'NURBSDiff/csrc/utils.cpp'],
                         include_dirs=[extensions_dir],
                         extra_compile_args=extra_compile_args),
            CppExtension(name='NURBSDiff.surf_eval_cpp',
                         sources=['NURBSDiff/csrc/surf_eval.cpp', 'NURBSDiff/csrc/utils.cpp'],
                         include_dirs=[extensions_dir],
                         extra_compile_args=extra_compile_args),
            CUDAExtension(name='NURBSDiff.curve_eval_cuda',
                          sources=['NURBSDiff/csrc/curve_eval_cuda.cpp', 'NURBSDiff/csrc/curve_eval_cuda_kernel.cu'],
                          include_dirs=[extensions_dir],
                          extra_compile_args=extra_compile_args),
            CUDAExtension(name='NURBSDiff.surf_eval_cuda',
                          sources=['NURBSDiff/csrc/surf_eval_cuda.cpp', 'NURBSDiff/csrc/surf_eval_cuda_kernel.cu'],
                          include_dirs=[extensions_dir],
                          extra_compile_args=extra_compile_args),
        ],
        cmdclass={
            'build_ext': BuildExtension
        },
        packages=find_packages(include=include_package, exclude=("examples*", "images*")))
except:
    print('installation of NURBSDiff with GPU wasnt successful, installing CPU version')
    setup(
        ext_modules=[
            CppExtension(name='NURBSDiff.curve_eval_cpp',
                         sources=['NURBSDiff/csrc/curve_eval.cpp', 'NURBSDiff/csrc/utils.cpp'],
                         include_dirs=[extensions_dir],
                         extra_compile_args=extra_compile_args),
            CppExtension(name='NURBSDiff.surf_eval_cpp',
                         sources=['NURBSDiff/csrc/surf_eval.cpp', 'NURBSDiff/csrc/utils.cpp'],
                         include_dirs=[extensions_dir],
                         extra_compile_args=extra_compile_args),
        ],
        cmdclass={
            'build_ext': BuildExtension
        },
        packages=find_packages(include=include_package, exclude=("examples*", "images*")))
