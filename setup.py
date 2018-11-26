#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""
from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup_requirements = ['pytest-runner', ]
test_requirements = ['pytest', ]

requirements = ['Click<8',
                'pathlib2; python_version < "3.4"',
                'backports.tempfile; python_version < "3.2"',
                'future-fstrings; python_version < "3.6"',
                'configparser; python_version < "3"',
                ]

extras_require = {
    'dev': ['bumpversion==0.5.3',
            'wheel==0.30.0',
            'tox==2.9.1',
            'coverage==4.5.1',
            'twine==1.10.0',
            'ipython',
            ],
    'test': test_requirements
}


setup(
    author="Nikolaos Ves",
    author_email='vesnikos@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Users',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        # 'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Python Boilerplate contains all the boilerplate you need to create a Python package.",
    entry_points={
        'console_scripts': [
            'wpgpDownload=wpgpDownload.cli:wpgp_download',
        ],
    },
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    keywords='wpgpDownload',
    name='wpgpDownload',
    package_dir={'.': 'wpgpDownload'},
    packages=find_packages(),
    setup_requires=setup_requirements,
    extras_require=extras_require,
    test_suite='pytest',
    tests_require=test_requirements,
    url='https://github.com/wpgp/wpgpDownloadPy',
    version='0.1.3',
    zip_safe=False,
    include_package_data=True
)
