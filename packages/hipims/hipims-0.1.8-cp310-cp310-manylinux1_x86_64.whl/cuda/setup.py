from setuptools import setup
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

CUDA_FLAGS = []

# define cuda extensions
ext_modules = [
    CUDAExtension(
        'euler_update', [
            'euler_update_Interface.cpp',
            'euler_update_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'fluxCal_1stOrder', [
            'fluxCal_1stOrder_Interface.cpp',
            'fluxCal_1stOrder_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'fluxCal_2ndOrder', [
            'fluxCal_2ndOrder_Interface.cpp',
            'fluxCal_2ndOrder_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'fluxMask', [
            'fluxMask_Interface.cpp',
            'fluxMask_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'frictionImplicit_andUpdate', [
            'frictionImplicit_andUpdate_Interface.cpp',
            'frictionImplicit_andUpdate_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'infiltration_sewer', [
            'infiltration_sewer_Interface.cpp',
            'infiltration_sewer_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'stationPrecipitation', [
            'stationPrecipitation_Interface.cpp',
            'stationPrecipitation_Kernel.cu',
        ],
    ),
    CUDAExtension(
        'timeControl', [
            'timeControl_Interface.cpp',
            'timeControl_Kernel.cu',
        ],
    ),
]

# INSTALL_REQUIREMENTS = ['numpy', 'torch', 'torchvision', 'scikit-image', 'tqdm', 'imageio']
setup(
    extra_compile_args={
        'cxx': ['-std=c++11', '-O2', '-Wall'],
        'nvcc': [
            '-std=c++11', '--expt-extended-lambda', '--use_fast_math',
            '-Xcompiler', '-Wall', '-gencode=arch=compute_60,code=sm_60',
            '-gencode=arch=compute_61,code=sm_61',
            '-gencode=arch=compute_70,code=sm_70',
            '-gencode=arch=compute_72,code=sm_72',
            '-gencode=arch=compute_75,code=sm_75',
            '-gencode=arch=compute_75,code=compute_75'
        ],
    },

    ext_modules=ext_modules,
    cmdclass={
        'build_ext': BuildExtension.with_options(no_python_abi_suffix=True)
    })
