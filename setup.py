import os

from setuptools import setup

#os.environ["__STRATOPY_IN_SETUP__"] = "True"  # noqa
#import stratopy  # noqa


with open("README.md", "r") as fp:
    LONG_DESCRIPTION = fp.read()

DESCRIPTION = LONG_DESCRIPTION.splitlines()[0].strip()

REQUIREMENTS = [
    "numpy",
    "netCDF4",
    "diskcache",
    "python-dateutil",
    "sh",
    "h5py"
]

setup(
    name="StratoPy",
    #version=stratopy.__version__,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    install_requires=REQUIREMENTS,
    author="Paula Romero",
    author_email="paula.romero@mi.unc.edu.ar",
    url="https://github.com/paula-rj/",
    py_modules=None,
    packages=[""],
    include_package_data=True,
    license="The MIT License",
    keywords=["cumulo", "clouds"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
    ],
)