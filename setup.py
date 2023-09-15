#!/usr/bin/python
#
from setuptools import setup, find_packages

setup(
    name='synack',
    version='1.0',
    description='Synack-python3',
    packages=find_packages(include=['synack', 'synack.*']),
    install_requires=[
        'netaddr',
        'pathlib2',
        'pyotp',
        'numpy',
        'requests',
        'selenium',
        'urllib3[socks]>=1.26,<3',
        'psycopg2-binary',
        'cmd2',
    ],
    entry_points={
        'console_scripts': [
            'synack = synack.__main__:main'
        ]
    }
)

