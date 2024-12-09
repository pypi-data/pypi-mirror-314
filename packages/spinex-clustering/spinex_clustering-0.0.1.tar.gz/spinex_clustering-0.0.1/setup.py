# File: setup.py
from setuptools import setup, find_packages

setup(
    name="spinex_clustering",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        'numpy>=1.19.0',
        'scipy>=1.6.0',
        'scikit-learn>=0.24.0',
        'numba>=0.53.0',
        'umap-learn>=0.5.0'
    ],
    python_requires='>=3.7',
)
