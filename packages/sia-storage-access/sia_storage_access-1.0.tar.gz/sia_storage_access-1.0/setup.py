from setuptools import setup, find_packages
from os.path import abspath, exists

build_number = 0
build_number_path = abspath("build.number")

if exists(build_number_path):
    build_number = open(build_number_path).read().strip()

setup(
    name='sia-storage-access',
    version='1.%s' % build_number,
    description='Sia Storage Access Layer',
    packages=find_packages(include=["sia_storage*"]),
    include_package_data=True,
    install_requires=[
        'azure-data-tables==12.6.0',
        'azure-storage-blob==12.24.0',
        'azure-storage-file-datalake==12.18.0'
    ],
    author='Data Stride Analytics',
    license='proprietary',
    url='https://github.com/sumalata23dsa/SIA_API_BACKEND',
    python_requires=">=3.8.0",
    readme="README.md"
)