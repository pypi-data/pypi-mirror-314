import configparser

from setuptools import setup, find_packages

config = configparser.ConfigParser()
config.read('./src/config/config.ini')

setup(
    name='mdocs',
    version=config['DEFAULT']['version'],
    packages=find_packages(where='src'),
    package_dir={'': 'src'}, 
    py_modules=['mdocs'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'mdocs=mdocs:main',
        ],
    },
    include_package_data=True,  
    package_data={
        'config': ['config.ini'],
    },
    author=config['DEFAULT']['author'],
    author_email='nomail@nomail.com',
    description='Allows to extract docstrings from Python functions to create a documentation file in Markdown format.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/rasamex/mdocs',  
    license='GPL-2.0 license'
)

'''
~/mdocs
python3 setup.py sdist
'''