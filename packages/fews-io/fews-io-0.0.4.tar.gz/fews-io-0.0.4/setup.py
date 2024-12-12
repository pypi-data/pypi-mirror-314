"""Library for communicating with Delft-FEWS

A library for reading and writing PI-XML files.
"""

import sys

from setuptools import find_packages, setup

import versioneer

DOCLINES = __doc__.split("\n")

CLASSIFIERS = """\
Development Status :: 4 - Beta
Intended Audience :: Science/Research
Intended Audience :: Information Technology
License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)
Programming Language :: Other
Topic :: Scientific/Engineering :: GIS
Topic :: Scientific/Engineering :: Mathematics
Topic :: Scientific/Engineering :: Physics
Operating System :: Microsoft :: Windows
Operating System :: POSIX
Operating System :: Unix
Operating System :: MacOS
"""

if sys.version_info < (3, 7):
    sys.exit("Sorry, Python 3.7 or newer is required.")

setup(
    name="fews-io",
    version=versioneer.get_version(),
    description=DOCLINES[0],
    classifiers=[_f for _f in CLASSIFIERS.split("\n") if _f],
    url="https://oss.deltares.nl/web/delft-fews",
    author="Tjerk Vreeken",
    author_email="tjerk.vreeken@deltares.nl",
    maintainer="Tjerk Vreeken",
    license="LGPLv3",
    keywords="fews deltares xml",
    platforms=["Windows", "Linux", "Mac OS-X", "Unix"],
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=["numpy >= 1.16.0"],
    tests_require=["pytest", "pytest-runner"],
    include_package_data=True,
    python_requires=">=3.7",
    cmdclass=versioneer.get_cmdclass(),
)
