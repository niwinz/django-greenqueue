#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name = 'django-greenqueue',
    version = ":versiontools:version:",
    description = "Asynchronous task queue/job queue based on distributed message passing",
    long_description = "",
    author = 'Andrei Antoukh',
    author_email = 'niwi@niwi.be',
    url = 'https://github.com/niwi/django-greenqueue',
    license = 'BSD',
    include_package_data = False,
    packages = find_packages(),
    zip_safe = False,
    install_requires=[
        'distribute',
    ],
    setup_requires = [
        'versiontools >= 1.9',
    ],
    classifiers = [
        'Framework :: Django',
        'Operating System :: POSIX',
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: BSD License',
        'Topic :: Communications',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Distributed Computing',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
