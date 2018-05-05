
from setuptools import setup
setup(
    name='commons_boundaries',
    version='0.1',
    description=(
        'A collection of tools to assist in creating boundaries in '
        'democratic commons repoistories'),
    url='https://github.com/everypolitician/commons-boundaries',
    author='mySociety',
    author_email='parliments@mysociety.org',
    license='MIT',
    packages=['commons_boundaries'],
    scripts=['bin/create-csv',
             'bin/create-config',
             'bin/create-boundary'],
    install_requires=[
        'fiona'
    ],
    extras_require={
        'testing': ['pytest']
    }
)
