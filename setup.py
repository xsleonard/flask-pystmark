#!/usr/bin/env python

"""
Flask-Pystmark
-------------

A Flask extension for Pystmark (a Postmark API library)
"""

from setuptools import setup

about = {}
with open('__about__.py') as f:
    exec(f.read(), about)

setup(
    name='Flask-Pystmark',
    version='0.1',
    url='https://github.com/xsleonard/flask-pystmark',
    license='MIT',
    author='Steve Leonard',
    author_email='sleonard76@gmail.com',
    description=about['description'],
    long_description=__doc__,
    py_modules=['flask_pystmark', '__about__'],
    zip_safe=False,
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Flask', 'pystmark'
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Communications :: Email',
        'Programming Language :: Python',
    ]
)
