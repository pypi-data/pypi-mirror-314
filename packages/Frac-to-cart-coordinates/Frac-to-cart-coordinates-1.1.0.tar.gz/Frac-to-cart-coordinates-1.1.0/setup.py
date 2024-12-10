from setuptools import setup, find_packages

setup(
    name='Frac-to-cart-coordinates', 
    version='1.1.0',  
    author='Noah Deveaux',
    author_email='noah.deveaux@unamur.be',
    description='A lightweight Python package for converting between fractional and Cartesian coordinates, supporting both forward and inverse transformations.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/n-deveaux/Frac-to-cart-coordinates',  
    packages=find_packages(), 
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'numpy',
    ],
)
