from setuptools import setup, find_packages

setup(
    name='NNimaker',
    version='3.0',
    packages=find_packages(where='.'),
    package_dir={'NNimaker': 'NNimaker'},
    install_requires=[
        #'numpy',
        #'pandas',
        #'json',
        #'collections',
        #'collections.abc',
        #'ase.data',
        #'glob',
    ],
    entry_points={
        'console_scripts': [
            'NNimake_QE = NNimaker:nnimake_qe',
        ],
    },
    author='Mandana Safari',
    author_email='m.safari@cineca.it',
    description='A module for processing user data to NN input',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://gitlab.hpc.cineca.it/msafari1/nnimaker.git',
)

