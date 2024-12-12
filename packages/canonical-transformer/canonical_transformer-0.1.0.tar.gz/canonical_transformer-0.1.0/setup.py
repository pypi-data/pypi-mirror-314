from setuptools import setup, find_packages

setup(
    name='canonical_transformer',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'python-dateutil'
    ],
    author='June Young Park',
    author_email='juneyoungpaak@gmail.com',
    description='A collection of utility functions for handling canonical transformations, facilitating efficient data processing and management.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nailen1/canonical_transformer.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
