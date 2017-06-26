
from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='apiaiassistant',

    version='1.0.0',

    description='Create API.ai agents in a heartbeat',
    long_description=long_description,

    url='TODO/apiaiassistant',

    author='Toaster LTD',
    author_email='developers@toasterltd.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Quality Assurance',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Communications :: Chat',
        'Topic :: Adaptive Technologies',
        'Topic :: Home Automation',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'

    ],

    keywords='apiai actionsongoogle voice home',

    py_modules=["apiaiassistant"],
)
