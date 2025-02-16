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
        "urllib3==1.26.6"
    ],
    py_modules=["main"],
    entry_points={"console_scripts": ["main = main:main"]},
)