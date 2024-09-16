import os

from setuptools import setup, find_packages

def get_version():
    return os.getenv("PACKAGE_VERSION", "0.0.0")

setup(
    name='emp-orderly-types',
    version=get_version(),
    python_requires='>=3.10, <3.13',
    install_requires=[
        'base58==2.1.1',
        'cryptography==42.0.5',
        'eth-typing==4.1.0',
        'eth-utils==4.1.0',
        'httpx==0.27.0',
        'pandas==2.2.2',
        'pydantic>=2.7.0',
        'python-dotenv==1.0.1',
        'requests==2.31.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)