import io
import os
import re

import setuptools

def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()
        
setuptools.setup(
    name='fastapi_tryton_integration',
    version='1.0.2',
    author='Solutema SRL',
    description='FastAPI connection module for Tryton ERP',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=['fastapi_tryton_integration', ],
    keywords='fastapi tryton',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Tryton',
        'Framework :: FastAPI',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='GPL-3',
    python_requires='>=3.10',
        install_requires=[
        'uvicorn',
        'fastapi==0.115.6',
        'pydantic==1.10.19',
        'trytond~=6.0.0',
    ])