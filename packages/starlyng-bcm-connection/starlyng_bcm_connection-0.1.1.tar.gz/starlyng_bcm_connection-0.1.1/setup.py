"""
setup.py
"""
from pathlib import Path
from setuptools import setup, find_packages

def read(file_path):
    """Read and return the contents of a file."""
    return Path(file_path).read_text(encoding='utf-8')

setup(
    name='starlyng_bcm_connection',
    version='0.1.1',
    packages=find_packages(exclude=['tests*']),
    extras_require={
        'dev': [
            'pytest',
            'pytest-mock==3.14.0',
            'pylint==3.2.2',
            'twine',
            'wheel',
        ],
    },
    author='Justin Sherwood',
    author_email='justin@sherwood.fm',
    description='A library for BCM functionality.',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    url='https://github.com/starlyngapp/ssh-connection',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: System :: Systems Administration',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
    license='MIT',
    keywords='bcm server management',
)
