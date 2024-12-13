# -*- coding: utf-8 -*-
# This file is part of the 'astrophysix' Python package.
#
# Copyright © Commissariat a l'Energie Atomique et aux Energies Alternatives (CEA)
#
#  FREE SOFTWARE LICENCING
#  -----------------------
# This software is governed by the CeCILL license under French law and abiding by the rules of distribution of free
# software. You can use, modify and/or redistribute the software under the terms of the CeCILL license as circulated by
# CEA, CNRS and INRIA at the following URL: "http://www.cecill.info". As a counterpart to the access to the source code
# and rights to copy, modify and redistribute granted by the license, users are provided only with a limited warranty
# and the software's author, the holder of the economic rights, and the successive licensors have only limited
# liability. In this respect, the user's attention is drawn to the risks associated with loading, using, modifying
# and/or developing or reproducing the software by the user in light of its specific status of free software, that may
# mean that it is complicated to manipulate, and that also therefore means that it is reserved for developers and
# experienced professionals having in-depth computer knowledge. Users are therefore encouraged to load and test the
# software's suitability as regards their requirements in conditions enabling the security of their systems and/or data
# to be ensured and, more generally, to use and operate it in the same conditions as regards security. The fact that
# you are presently reading this means that you have had knowledge of the CeCILL license and that you accept its terms.
#
#
# COMMERCIAL SOFTWARE LICENCING
# -----------------------------
# You can obtain this software from CEA under other licencing terms for commercial purposes. For this you will need to
# negotiate a specific contract with a legal representative of CEA.
#
from __future__ import unicode_literals
from setuptools import setup, find_packages


setup(
    name="astrophysix",
    version="0.7.1",  # Also found in astrophysix.__init__.py and in doc/source/conf.py
    install_requires=[
        'enum34;python_version<"3.4"',
        'pytz>=2019.1;python_version<"3.4"',
        'h5py>=2.10.0',
        'future>=0.17.1',
        'numpy>=1.16.4',
        'Pillow>=6.2.1',
        'pandas>=0.24.2'
    ],
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',  # 2.7.x or 3.5/3.6/3.7/3.8/3.9/3.10
    packages=find_packages(include=['astrophysix', 'astrophysix.*']),
    package_data={'astrophysix': ["astrophysix/simdm/d3_web/plot*.html",
                                  "astrophysix/simdm/d3_web/MathJax_local.js",
                                  "astrophysix/simdm/d3_web/d3_plot.gif",
                                  "astrophysix/simdm/d3_web/loading.png",
                                  # "tests/simdm/io/*"
    ]},
    include_package_data=True,

    # Metadata to display on PyPI
    author="Damien CHAPON",
    description="Astrophysical simulation project documentation package",
    long_description="""Astrophysical simulation project documentation tool. Lets the user create scientific analysis 
                        study portable HDF5 files based on the IVOA Simulation Datamodel standard. It also allow users
                        to handle some common and most useful physical quantities and units.""",
    author_email="damien.chapon@cea.fr",
    license="CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1, http://www.cecill.info)",

    keywords="Astrophysics simulation analysis publication",
    url="https://astrophysix.readthedocs.io",
    download_url="https://gitlab.com/coast-dev/astrophysix",
    project_urls={
        "Source": "https://drf-gitlab.cea.fr/coast-dev/Astrophysix/",
    },

    classifiers=["Intended Audience :: Science/Research",
                 "License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)",
                 "Operating System :: MacOS :: MacOS X",
                 "Operating System :: POSIX :: Linux",
                 # "Development Status :: 3 - Alpha",
                 # "Development Status :: 4 - Beta",
                 "Development Status :: 5 - Production/Stable",
                 "Programming Language :: Python :: 2.7",
                 "Programming Language :: Python :: 3.6",
                 "Programming Language :: Python :: 3.7",
                 "Programming Language :: Python :: 3.8",
                 "Programming Language :: Python :: 3.9",
                 "Programming Language :: Python :: 3.10",
                 "Topic :: Software Development :: Version Control :: Git",
                 "Topic :: Scientific/Engineering :: Physics",
                 "Topic :: Scientific/Engineering :: Astronomy",
                 "Topic :: Scientific/Engineering :: Information Analysis"],
    entry_points={
        "console_scripts": [
            "gald3_server = astrophysix.simdm.d3_web.__main__:main"
        ]
    },
)
