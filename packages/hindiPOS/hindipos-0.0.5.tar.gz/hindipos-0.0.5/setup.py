from setuptools import setup, find_packages
from os import path

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='hindiPOS',
    version='0.0.5',
    #url='https://github.com/yourname/yourproject',
    author='Devanshi',
    author_email='devanshiisuri@gmail.com',
    description='POS tagger for hindi language',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['hindiPOS'],  #auto_discover packages
    package_data={'hindiPOS': ['*.csv']},
    install_requires=['polars'],
    include_package_data=True,
)
