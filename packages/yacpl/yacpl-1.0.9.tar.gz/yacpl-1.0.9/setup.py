from setuptools import setup, find_packages

# read the contents of your README file.
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='yacpl',
	version='1.0.9',
    packages=find_packages(),
	package_dir={'': '.'},
    long_description=long_description,
    long_description_content_type='text/markdown'
)
