from setuptools import setup, find_packages

setup(
    name="svnm",
    version="0.1.2",
    author="svn.murali",
    author_email="svnmurali1@gmail.com",
    description="A package to make the usage of DeepLearning models easier",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/svnmurali-2004/svnm",  # Replace with your GitHub URL
    
    install_requires=[
       "huggingface_hub==0.26.5",
"matplotlib==3.9.3",
"numpy==2.2.0",
"pyfiglet==1.0.2",
"setuptools==75.1.0",
"tensorflow==2.18.0",
"termcolor==2.5.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
