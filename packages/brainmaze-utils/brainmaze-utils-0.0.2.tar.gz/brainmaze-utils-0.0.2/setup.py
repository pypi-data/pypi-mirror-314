# Copyright 2020-present, Mayo Clinic Department of Neurology
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.


import setuptools
from glob import glob

from setuptools import Command, Extension
import shlex
import subprocess
import os
import re

## get version from file
VERSIONFILE="./brainmaze_utils/__init__.py"
verstrline = open(VERSIONFILE, "rt").read()
VSRE = r"^__version__ = ['\"]([^'\"]*)['\"]"
mo = re.search(VSRE, verstrline, re.M)
if mo:
    verstr = mo.group(1)
else:
    raise RuntimeError("Unable to find version string in %s." % (VERSIONFILE,))

setuptools.setup(
    name="brainmaze-utils",
    version=verstr,
    license='',
    url="https://github.com/bnelair/brainmaze_utils",

    author="Filip Mivalt",
    author_email="mivalt.filip@mayo.edu",


    description="BrainMaze: Brain Electrophysiology, Behavior and Dynamics Analysis Toolbox",
    long_description="Frequently used functions supporting the BrainMaze package, so the full package does not need to be installed in full size everytime.",
    long_description_content_type="",

    packages=setuptools.find_packages(),
    include_package_data=True,

    classifiers=[
        "Development Status :: 3 - Alpha",
        'Intended Audience :: Healthcare Industry',
        'Intended Audience :: Science/Research',
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Operating System :: POSIX :: Linux",
        'Topic :: Scientific/Engineering :: Medical Science Apps.'
    ],
    python_requires='>=3.6',
    install_requires =[
        'numpy',
        'scipy',
        'pandas',
        'scikit-learn',
        'tqdm',
        'matplotlib'
    ]
)






