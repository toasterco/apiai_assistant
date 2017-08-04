
from setuptools import setup
from codecs import open
from os import path

VERSION = '0.1.0'

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, 'README.rst'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='apiai_assistant',

    version=VERSION,

    description='Create API.ai agents in a heartbeat',
    long_description=LONG_DESCRIPTION,

    url='https://github.com/toasterco/apiaiassistant',

    author='Zack Dibe',
    author_email='contact@zackdibe.com',

    maintainer='Toaster LTD developers',
    maintainer_email='developers@toasterltd.com',

    platforms=['any'],
    packages=['apiai_assistant'],

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

    keywords='apiai actionsongoogle alexa messenger voice home',

    py_modules=["apiai_assistant"],
)
