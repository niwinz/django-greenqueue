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
    setup_requires = [
        'versiontools >= 1.9',
    ],
    classifiers = [
        'Development Status :: 4 - Beta',
        "Programming Language :: Python",
        'Operating System :: POSIX',
        'Framework :: Django',
        'License :: OSI Approved :: BSD License',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: System :: Distributed Computing',
        'Topic :: Communications',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
    ]
)
