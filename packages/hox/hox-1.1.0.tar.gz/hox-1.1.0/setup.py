import os
from setuptools import setup

directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(directory, 'README.md'), encoding='utf-8') as f:
  long_description = f.read()

setup(
    name='hox',
    version='1.1.0',
    license='MIT',
    url = 'https://github.com/usedToBeTomas/hox',
    author='usedToBeTomas',
    description='Lightweight neual network library project.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['hox'],
    python_requires='>=3.6',
    keywords = ['neural network', 'ml', 'ai', 'machine learning','vanilla','nn'],
    install_requires=[
        'numpy',
        'tqdm'
    ],
)
