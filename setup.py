from setuptools import setup, find_packages

setup(
    name='svgast',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    decsription='Helpers for building SVG files in Python',
    keywords=['svg', 'xml'],
    url='http://github.com/concert/svgast',
    author='Paul Weaver',
    author_email='paul@concertdaw.co.uk',
    version='0.0.0',
    license='',
    install_requires=[
        'lxml'
    ],
    extras_require={
        'test': ['flake8', 'pytest', 'pytest-cov']
    }
)
