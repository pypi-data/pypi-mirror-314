import platform
from setuptools import setup, find_packages

def read_file(filename):
    with open(filename) as f:
        return f.read()
        
version=read_file('iFinDAPI/VERSION.txt')

setup(
    name='iFinDAPI',
    version=version,
    python_requires='>=3.7',
    description='THS_DataInterface SDK API',
    long_description=read_file('README.md'),
    long_description_content_type='text/markdown',
    url='https://quantapi.51ifind.com/',
    packages=find_packages(),
    author='ifind',
    author_email='ifind_webexcel@myhexin.com',
    keywords='iFinDAPI, datainterface, FTDI, iFinDSDK, thsAPI',
    license='Apache License v2',
    install_requires=[
        'numpy',
        'pandas'
    ],
    package_data={
        '': ['*.dll','*.xml','*.ini','*.so','*.manifest'],
    },
    py_modules=['iFinDPy'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: Unix'
    ],
)
