#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [ "hvac>=0.9.5", "requests>=2.22.0" ]

setup_requirements = [ ]

test_requirements = [ ]

setup(
    author="Steve Graham",
    author_email='stgraham2000@gmail.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Read from a KV-2 secret path in Vault and create a .env file from the list of key/value pairs.",
    entry_points={
        'console_scripts': [
            'vault2env=vault2env.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='vault2env',
    name='vault2env',
    packages=find_packages(include=['vault2env', 'vault2env.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/stgraham2000@gmail.com/vault2env',
    version='0.11.0',
    zip_safe=False,
)
