# -*- coding: utf-8 -*-
from setuptools import setup


setup(
    name='gdp',
    version='0.1',
    description='Grab data persistence layer',
    url='http://github.com/istinspring/gdp',
    author='Alex Istinspring',
    author_email='istinspring@gmail.com',
    license='MIT',
    packages=['gdp'],
    install_requires=[
        'cerberus',
    ],
    zip_safe=False
)
