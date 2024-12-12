# setup.py

from setuptools import setup, find_packages

setup(
    name="duckbin",  
    version="1.0.1",  
    packages=find_packages(),  
    install_requires=["requests"],  
    description="This package allows you to save any text for free on our servers. Whether it's a note, an article, or any other type of content, you can easily store it without any cost.",
    long_description=open("README.md").read(), 
    long_description_content_type="text/markdown", 
    author="freeutka",
    author_email="freeutka@inbox.lv",
    url="https://github.com/freeutka/DuckBin", 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)