from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.0-beta'
DESCRIPTION = 'iLOSCAR'
LONG_DESCRIPTION = 'A web-based interactive carbon cycle model, built upon the classic LOSCAR model.'

# Setting up
setup(
    name="iloscar",
    version=VERSION,
    url = 'https://github.com/Shihan150/iloscar',
    license = 'MIT',
    author="Shihan Li",
    author_email="<shihan@tamu.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=['iloscar', 'iloscar/pages'],
    install_requires=['numpy', 'scipy', 'dash', 'plotly', 'pandas', 'numba', 'diskcache', 'statsmodels', 'dash_bootstrap_components','dash_extensions','dash[diskcache]', 'dill == 0.3.5.1'],
    keywords=['python', 'carbon cycle', 'model', 'paleoclimate', 'global warming', 'LOSCAR'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],

    include_package_data = True,
    package_data = {
    'iloscar': ['dat_y0/*.dat']
    },
    python_requires='>3.7, <3.11'

)
