import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

setup(
    name='score.mustache',
    version='0.0.1',
    description='Mustache renderer of The SCORE Framework',
    long_description=README,
    author='strg.at',
    author_email='score@strg.at',
    url='http://score-framework.org',
    keywords='score framework javascript mustache',
    packages=['score', 'score.mustache'],
    namespace_packages=['score'],
    zip_safe=False,
    license='LGPL',
    install_requires=[
        'score.init',
        'score.js>=0.3.0',
        'score.http>=0.2.6',
        'pystache',
    ],
)
