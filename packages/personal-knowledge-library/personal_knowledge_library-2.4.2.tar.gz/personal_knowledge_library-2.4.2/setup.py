#!/usr/bin/env python
import pathlib
import sys
from setuptools import setup, find_packages

CURRENT_PYTHON = sys.version_info[:2]
REQUIRED_PYTHON = (3, 7)

if CURRENT_PYTHON < REQUIRED_PYTHON:
    sys.stderr.write(f"""
    ==========================
    Unsupported Python version
    ==========================
    This version of personal knowledge lib requires Python {REQUIRED_PYTHON}.
    
    This may be because you are using a version of pip that doesn't
    understand the python_requires classifier. Make sure you
    have pip >= 9.0 and setuptools >= 24.2, then try again:
        $ python -m pip install --upgrade pip setuptools
    This will install the latest version of personal-knowledge-library which works on your
    version of Python. If you can't upgrade your pip (or Python), request
    an older version of knowledge-service-lib :
        $ python -m pip install personal-knowledge-library
    """)
    sys.exit(1)

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# the setup
setup(
    name='personal_knowledge_library',
    version="2.4.2",
    description="Library to access Wacom's Personal Knowledge graph.",
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/Wacom-Developer/personal-knowledge-library',
    author='Markus Weber',
    author_email='markus.weber@wacom.com',
    license='Apache 2.0 License',
    keywords='semantic-knowledge;knowledge-graph',
    packages=find_packages(exclude=('docs', 'tests', 'env')),
    include_package_data=True,
    install_requires=[
        "requests>=2.32.0",
        "python-dateutil>=2.8.2",
        "PyJWT>=2.6.0",
        "tqdm>=4.66.3",
        "ndjson>=0.3.1",
        "rdflib>=6.3.2",
        "aiohttp[speedups]>3.10.11",
        "orjson>=3.8.0",
        "cachetools==5.3.2"
    ],
    extras_require={
    },
    tests_require=(
        'pytest==8.3.3',
        'pytest-asyncio==0.23.7',
        'pytest-cov==1.1.3',
        'faker==21.0.0',
        'ontospy==2.1.1',
        'pytest-env==1.1.3'
    ),
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Operating System :: OS Independent",
        "Natural Language :: English",
    ]
)
