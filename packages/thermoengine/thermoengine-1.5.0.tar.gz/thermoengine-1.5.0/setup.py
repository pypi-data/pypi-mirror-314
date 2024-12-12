#!/usr/bin/env python
""" file: setup.py
    modified: Mark S. Ghiorso, OFM Research
    date: June 12, 2017, rev June 27, 2017, rev cython Dec 19, 2019, rev Dec 31, 2022

    description: Distutils installer script for thermoengine.
"""
from setuptools import setup, find_packages
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy

from sys import platform
if platform == "linux" or platform == "linux2":
    from distutils import sysconfig
elif platform == "darwin":
    pass
elif platform == "win32":
    pass

extensions = [
    Extension(
        "thermoengine.aqueous",
        sources=["thermoengine/aqueous/aqueous.pyx",
        "thermoengine/aqueous/swim.c",
        "thermoengine/aqueous/born.c",
        "thermoengine/aqueous/duanzhang.c",
        "thermoengine/aqueous/holten.c",
        "thermoengine/aqueous/wagner.c",
        "thermoengine/aqueous/zhangduan.c",
        "thermoengine/aqueous/FreeSteam2.1/b23.c",
        "thermoengine/aqueous/FreeSteam2.1/backwards.c",
        "thermoengine/aqueous/FreeSteam2.1/bounds.c",
        "thermoengine/aqueous/FreeSteam2.1/common.c",
        "thermoengine/aqueous/FreeSteam2.1/derivs.c",
        "thermoengine/aqueous/FreeSteam2.1/region1.c",
        "thermoengine/aqueous/FreeSteam2.1/region2.c",
        "thermoengine/aqueous/FreeSteam2.1/region3.c",
        "thermoengine/aqueous/FreeSteam2.1/region4.c",
        "thermoengine/aqueous/FreeSteam2.1/solver2.c",
        "thermoengine/aqueous/FreeSteam2.1/steam.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_ph.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_ps.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_pT.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_pu.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_pv.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_Ts.c",
        "thermoengine/aqueous/FreeSteam2.1/steam_Tx.c",
        "thermoengine/aqueous/FreeSteam2.1/surftens.c",
        "thermoengine/aqueous/FreeSteam2.1/thcond.c",
        "thermoengine/aqueous/FreeSteam2.1/viscosity.c",
        "thermoengine/aqueous/FreeSteam2.1/zeroin.c"],
        include_dirs=['./thermoengine/aqueous', './thermoengine/aqueous/FreeSteam2.1', numpy.get_include()],
        extra_compile_args=['-O3', '-DNPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION'],
        libraries=['gsl'],
        library_dirs=['/usr/local/lib'],
        runtime_library_dirs=['/usr/local/lib']
    ),
]

if platform == "linux" or platform == "linux2":
    sysconfig.get_config_vars()['CC'] = 'clang'
    sysconfig.get_config_vars()['CXX'] = 'clang++'
    sysconfig.get_config_vars()['CCSHARED'] = '-fPIC'
    sysconfig.get_config_vars()['LDSHARED'] = 'clang -shared'

def readme():
    with open('README.rst') as f:
        return f.read()


setup(
      name='thermoengine',
      version='1.5',
      description='Principal Python package for ENKI thermodynamics modules',
      long_description=readme(),
      url='http://gitlab.com/enki-portal/ThermoEngine',
      author='Aaron S. Wolf; Mark S. Ghiorso',
      author_email='aswolf@umich.edu, ghiorso@ofm-research.org',
    #   license='GNU AFFERO GENERAL PUBLIC LICENSE Version 3',
      license='GNU Affero General Public License v3',
      packages=find_packages(where='.'),
    #   packages=[
    #       'thermoengine','thermoengine.aqueous',
    #   ],
      ext_modules = cythonize(extensions),
      include_package_data=True,
      install_requires=[
         'arrow>=1.2.3',
         'asks>=3.0.0',
         'cmake>=3.25.0',
         'coverage>=7.0.0',
         'cython>=0.29.32',
         'deprecation>=2.1.0',
         'elasticsearch>=6.3.1',
         'elasticsearch-dsl>=6.1.0',
         'fqdn>=1.5.1',
         'ipykernel>=6.19.4',
         'isoduration>=20.11.0',
         'jsonpointer>=2.0',
         'jupyter>=1.0.0',
         'jupyterlab>=3.5.2',
         'matplotlib>=3.6.2',
         'nbval>=0.9.6',
         'nptyping>=2.4.1',
         'numdifftools>=0.9.41',
         'numpy>=1.24.0',
         'openpyxl>=3.0.10',
         'pandas>=1.5.2',
         'pytest>=7.2.0',
         'pytest-cov>=4.0.0',
         'qtconsole>=5.4.0',
         'qtpy>=2.3.0',
         'rfc3339-validator>=0.1.4',
         'rfc3986-validator>=0.1.1',
         'scipy>=1.9.3',
         'seaborn>=0.12.1',
         'statsmodels>=0.13.5',
         # 'sulfLiq>=1.0.3',
         'sympy>=1.11.1',
         'trio>=0.22.0',
         'uri-template>=1.2.0', 
         'webcolors>=1.12',
      ],
      classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Chemistry',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Software Development :: Libraries :: Python Modules'
      ],
      zip_safe=False,
      test_suite='nose.collector',
      tests_require=['nose']
)
