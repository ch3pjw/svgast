from setuptools import setup

setup(
    name='svgast',
    packages=['svgast'],
    decsription='Helpers for building SVG files in Python',
    keywords=['svg', 'xml'],
    url='http://github.com/concertdaw/svgast',
    author='Paul Weaver',
    author_email='paul@concertdaw.co.uk',
    version='0.0.0',
    license='',
    install_requires=[
        'lxml'
    ],
    extras_require={
        'test': ['pytest']
    }
)
