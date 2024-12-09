from setuptools import setup, find_packages

setup(
    name='varoon',
    version='0.2.0',
    description='A tool for checking reflected parameters in URLs',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Eshan Singh',
    author_email='r0x4r@yahoo.com',
    url='https://github.com/R0X4R/varoon',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.1',
    ],
    entry_points={
        'console_scripts': [
            'varoon=varoon.main:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
