"""setup"""
from setuptools import find_packages, setup

setup(
    name='ezKit',
    version='1.7.5',
    author='septvean',
    author_email='septvean@gmail.com',
    description='Easy Kit',
    packages=find_packages(exclude=['documents', 'tests']),
    include_package_data=True,
    python_requires='>=3.11'
    # install_requires=[
    #     'loguru>=0.7.0',
    #     'tomlkit>=0.12.0'
    # ]
)
