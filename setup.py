from setuptools import setup, find_packages

setup(
    name="pandas_cache",  # this line is important.
    author="Zach Estela",
    author_email="z@aracel.io",
    install_requires=["pandas"],  
    packages=find_packages(),  
    decription="decorator for smart caching of results from functions that return dataframes",
    zipsafe=False
)