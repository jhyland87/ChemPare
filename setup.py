from setuptools import setup

setup(
    name="ChemPare",
    version="0.0.0",
    install_requires=[
        "requests",
        "bs4",
        "rich",
        "abcplus",
        "typing",
        "enum34",
        "urllib3==1.26.6",
        "dataclasses",
        "numpy",
        "pathlib",
        "curl_cffi",
        "translate",
        "pytest",
        "regex",
    ],
    py_modules=["chempare"],
    #entry_points={"console_scripts": ["main = main:main"]},
)
