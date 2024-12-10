from setuptools import setup, find_packages
import os

# Get the directory where setup.py is located
here = os.path.abspath(os.path.dirname(__file__))

# Read the contents of README.md for the long_description
with open(os.path.join(here, "README.md"), "r", encoding="utf-8") as fh:
    long_description = fh.read()
        
setup(
    name="abotaleb1",
    version="2.0.0",
    packages=find_packages(),
    include_package_data=True,  # Ensure non-Python files are included
    package_data={
        "my_models": ["input.txt"],  # Specify the input file to include
    },
    install_requires=[],
    author="Mostafa Abotaleb",
    author_email="abotalebmostafa@bk.ru",
    description=(
        "A Python library for modeling univariate time series using the "
        "Generalized Least Deviation Method (GLDM) First, and Second orders."
        "Generalized Least Deviation Method High Order (GLDMHO) Third, Fourth, and Fifth orders."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",  # Ensures proper rendering on PyPI
    url="https://github.com/abotalebmostafa11/GLDMHO",  # Pointing to the repository root
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",  # Added additional Python versions
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    license="MIT",  # Explicitly specifying the license
    python_requires='>=3.9',  # Specify the Python versions you support
    project_urls={  # Optional: Additional links
        "Bug Reports": "https://github.com/abotalebmostafa11/GLDMHO/issues",
        "Source": "https://github.com/abotalebmostafa11/GLDMHO",
    },
)
