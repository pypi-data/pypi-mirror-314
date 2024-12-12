from setuptools import setup, find_packages

setup(
    name="svnm",
    version="0.1.0",
    author="Your Name",
    author_email="svnmurali1@gmail.com",
    description="A simple package to greet users",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/svnmurali-2004/svnm",  # Replace with your GitHub URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
