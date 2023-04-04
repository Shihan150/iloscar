from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.1'
DESCRIPTION = 'iLOSCAR'
LONG_DESCRIPTION = 'A web-based interactive carbon cycle model, built upon the classic LOSCAR model.'

# Setting up
setup(
    name="iloscar",
    version=VERSION,
    author="Shihan Li",
    author_email="<shihan@tamu.edu>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy', 'scipy', 'dash', 'plotly', 'pandas', 'numba', 'diskcache', 'statsmodels', 'dash_bootstrap_components', 'collections'],
    keywords=['python', 'carbon cycle', 'model', 'paleoclimate', 'global warming', 'LOSCAR'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
