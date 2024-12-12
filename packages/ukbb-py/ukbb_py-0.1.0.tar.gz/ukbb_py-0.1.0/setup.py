from setuptools import setup, find_packages

setup(
    name='ukbb_py',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'seaborn',
        'statsmodels',
        'polars',
        'pyarrow',
        'fastparquet',
        ''
    ],
    url='https://github.com/Surajram112/UKBB_py',
    author='Suraj Ramchand',
    author_email='surajnramchand@gmail.com',
    description='An ensemble of functions for analysing UKBB records on DNA Nexus.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)