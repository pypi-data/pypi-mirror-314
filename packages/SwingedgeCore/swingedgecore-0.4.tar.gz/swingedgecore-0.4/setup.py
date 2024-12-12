from setuptools import setup, find_packages

setup(
    name='SwingedgeCore',
    version='0.4',
    author='Syptus',
    author_email='info@syptus.com',
    packages=find_packages(),  
    include_package_data=True,
    install_requires=['boto3'], 
    description='A package for utility functions used in SwingEdge Project',
    url='https://github.com/dhirs/swingedge_core',
)