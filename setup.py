"""
To build with coverage of Cython files
export SM_CYTHON_COVERAGE=1
python -m pip install -e .
pytest --cov=statsmodels statsmodels
coverage html
"""
from setuptools import find_packages, setup
from setuptools.dist import Distribution

from collections import defaultdict
import fnmatch
import os
from os.path import join as pjoin, relpath


##############################################################################
# Construct package data
##############################################################################
package_data = defaultdict(list)
filetypes = ["*.csv", "*.txt", "*.dta"]
for root, _, filenames in os.walk(
    pjoin(os.getcwd(), "statsmodels", "datasets")
):  # noqa: E501
    matches = []
    for filetype in filetypes:
        for filename in fnmatch.filter(filenames, filetype):
            matches.append(filename)
    if matches:
        package_data[".".join(relpath(root).split(os.path.sep))] = filetypes
for root, _, _ in os.walk(pjoin(os.getcwd(), "statsmodels")):
    if root.endswith("results"):
        package_data[".".join(relpath(root).split(os.path.sep))] = filetypes

if os.path.exists("MANIFEST"):
    os.unlink("MANIFEST")


INSTALL_REQUIRES = []
with open("requirements.txt", encoding="utf-8") as req:
    for line in req.readlines():
        INSTALL_REQUIRES.append(line.split("#")[0].strip())


setup(
    name='statsmodels',
    packages=find_packages(),
    package_data=package_data,
    include_package_data=False,  # True will install all files in repo
    zip_safe=False,
    python_requires=">=3.8",
    install_requires=INSTALL_REQUIRES,
)
