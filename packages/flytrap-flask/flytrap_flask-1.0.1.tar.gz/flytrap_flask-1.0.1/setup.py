from setuptools import setup, find_packages
import pathlib

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# Read the README file for the long description
README = (HERE / "README.md").read_text()

setup(
    name="flytrap_flask",
    version="1.0.1",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/getflytrap/flytrap_flask",
    packages=find_packages(),
    install_requires=[
        "Flask",
        "requests",
    ],
    python_requires=">=3.6",
    project_urls={  
        "Homepage": "https://getflytrap.github.io/",
    },
)
