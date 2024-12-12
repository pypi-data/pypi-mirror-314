from setuptools import setup, find_packages

setup(
    name="my_sample_king",  
    version="0.1.0",  
    author="king",
    author_email="swolf0512@gmail.com",
    description="A simple sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/king/my_sample_king", 
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
