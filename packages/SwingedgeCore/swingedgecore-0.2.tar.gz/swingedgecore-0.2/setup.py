from setuptools import setup, find_packages

setup(
    name='SwingedgeCore',
    version='0.2',
    author='Syptus',
    author_email='info@syptus.com',
    packages=find_packages(include=['SwingedgeCore', 'SwingedgeCore.*']),  # Finds all sub-packages
    include_package_data=True,  # Ensures non-Python files are included
    package_data={
        '': ['*.py'],  # Include all Python files
    },
    install_requires=['boto3'],  # Dependencies
    description='A package for utility functions used in SwingEdge Project',
    url='https://github.com/dhirs/swingedge_core',
)