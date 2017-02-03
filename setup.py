# -*- coding: UTF-8 -*-
from setuptools import setup, find_packages

setup(
    name='billomat',
    packages=find_packages(),
    version='0.1.31',
    description='billomat.com API client',
    author='Jens Nistler',
    author_email='opensource@jensnistler.de',
    url='http://jensnistler.de/',
    download_url='http://github.com/lociii/billomat',
    keywords=['billomat', 'api', 'client'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development',
    ],
    install_requires=[
        'requests>=2.1.0',
        'six>=1.4.1',
        'python-dateutil>=2.2',
        'httmock>=1.0.7',
        'mock>=1.0.1',
    ],
    include_package_data=True,
    long_description=open('README.md').read()
)
