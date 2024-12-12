from setuptools import setup, find_packages

setup(
    name='canonical_transformer',
    version='0.1.3',
    packages=find_packages(),
    install_requires=[
        'numpy>=2.1.3',
        'pandas>=2.2.3',
        'python-dateutil>=2.9.0',
        'pytz>=2024.2',
        'typing_extensions>=4.12.2'
    ],
    author='June Young Park',
    author_email='juneyoungpaak@gmail.com',
    description='A Python module for canonical data transformations between different data types and formats. Provides standardized mappings between DataFrames, dictionaries, files, and other data structures.',
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
