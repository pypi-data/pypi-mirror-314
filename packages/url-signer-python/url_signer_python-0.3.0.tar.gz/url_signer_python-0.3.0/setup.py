# pylint: disable=consider-using-with
from setuptools import setup, find_packages

setup(
    name='ioriver-url-signer',
    version='0.3.0',
    description='A Python library to sign URLs',
    author='IO River',
    author_email='support@ioriver.io',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'akamai-edgeauth>=0.3.2',
        'cryptography>=44.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.9'
        # 'License :: OSI Approved :: MIT License',
        # 'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
    include_package_data=True  # This will include files listed in MANIFEST.in
)
