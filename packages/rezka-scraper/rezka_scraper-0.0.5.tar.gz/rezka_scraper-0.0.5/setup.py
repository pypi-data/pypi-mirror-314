# setup.py

import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name='rezka_scraper',
    version='0.0.5',
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'beautifulsoup4',
    ],
    python_requires='>=3.8',
    description='RezkaScraper — это мини библиотека на Python для асинхронного поиска контента (аниме, фильмов, сериалов и мультфильмов) на сайте Rezka.ag',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='OFFpolice',
    author_email='offpolice2077@gmail.com',
    url='https://github.com/OFFpolice/rezka_scraper',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
