# Setup script for the metar package
# $Id: setup.py,v 1.3 2006/08/01 16:10:29 pollard Exp $
#
# Usage: python setup.py install
#
import os
from setuptools import setup, find_packages

def getDataFiles(submodule, folder):
    datadir = os.path.join('.', submodule, folder)
    files = [d for d in map(
        lambda x: os.path.join(datadir, x),
        os.listdir(datadir)
    )]
    return files

# DATA_FILES = [
#     ('metar_data/test_data', getDataFiles('.',  'test')),
#     ('metar_data/reference', getDataFiles('.', 'reference')),
#     #('pybmp_data/nsqd', getDataFiles('nsqd', 'data')),
# ]

# PACKAGE_DATA = {
#     'metar/reference': ['reference/*'],
#     'metar/testing': ['test/*']
# }

DESCRIPTION = "Modifies SWMM input files"

LONG_DESCRIPTION = "Inserts crazy subcatchments between nodes in a SWMM model"

setup(
    name="swmmdoodler",
    version="0.1.0",
    author="Lucas Nguyen",
    author_email="lnguyen@geosyntec.com",
    url="http://www.geosyntec.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    # package_data=PACKAGE_DATA,
    # data_files=DATA_FILES,
    download_url="http://www.geosyntec.com",
    license="MIT",
    packages=find_packages(exclude=[]),
    platforms="Python 2.7 and later.",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Intended Audience :: Science/Research",
#        "Topic :: Formats and Protocols :: Data Formats",
#        "Topic :: Scientific/Engineering :: Earth Sciences",
#        "Topic :: Software Development :: Libraries :: Python Modules"
        ]
    )
