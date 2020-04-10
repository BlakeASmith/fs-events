import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent

readme = (here / 'README.rst').read_text()

setup(
        name='fs-events',
        version="0.0.4",
        description='Expose filesystem events as generators',
        long_description=readme,
        long_description_content_type='text/x-rst',
        url='https://github.com/BlakeASmith/fs-events',
        author='Blake Smith',
        classifiers=[
            "Programming Language :: Python :: 3"
        ],
        packages=find_packages(),
)
