from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.2"
DESCRIPTION = "Agent Based Modelling Environment"
LONG_DESCRIPTION = "A package enabling Transport ABM."

# Setting up
setup(
    name="sysame",
    version=VERSION,
    author="Mahmoud Ishtaiwi",
    author_email="<m.ishtaiwe@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "numpy",
        "polars",
        "scipy",
        "pyarrow",
        "pandas",
        "matplotlib",
    ],
    keywords=["python", "abm", "transport", "modelling", "environment"],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
