from setuptools import setup, find_packages
import os

def read_readme():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as f:
        return f.read()

setup(
    name='anbuapis',
    version='1.0.0',
    description='A Python module for interacting with the api.anbuinfosec.xyz',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='Mohammad Alamin',
    author_email='anbuinfosec@gmail.com',
    url='https://github.com/anbuinfosec/anbuapis',
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
