from setuptools import setup

setup(
    name="hello-world-sample",  
    version="0.1.0",
    author="dp",
    author_email="dp@gmail.com",
    description="A simple Hello World package",
    py_modules=["hello"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
