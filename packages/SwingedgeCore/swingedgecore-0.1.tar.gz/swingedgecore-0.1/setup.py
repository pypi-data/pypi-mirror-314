from setuptools import setup, find_packages

setup(
    name='SwingedgeCore',
    version='0.1',
    author="Syptus",
    author_email="info@syptus.com",
    packages=find_packages(include=['SwingedgeCore','SwinedgeCore.*']),
    install_requires=['boto3'],
    description='A package for utility functions used in SwingEdge Project',
    url='https://github.com/dhirs/swingedge_core',
)
