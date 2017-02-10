from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


version = '0.1'


setup(
    name='nwscan',
    version=version,
    description='Scan networks for alive hosts',
    long_description=long_description,
    author='Pedro Buteri Gonring',
    author_email='pedro@bigode.net',
    url='https://github.com/pdrb/nwscan',
    license='MIT',
    classifiers=[],
    keywords='scan scanner network networks ip ips host hosts alive nwscan',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['ipaddr'],
    entry_points={
        'console_scripts': ['nwscan=nwscan.nwscan:cli'],
    },
)
