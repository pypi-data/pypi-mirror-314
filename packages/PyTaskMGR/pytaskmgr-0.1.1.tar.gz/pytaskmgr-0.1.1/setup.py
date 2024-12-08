from setuptools import setup, find_packages

setup(
    name="PyTaskMGR",
    version="0.1.1",
    packages=find_packages(),
    description="A Python library to manage system processes and gather system information.", 
    long_description=open('README.md').read(), 
    long_description_content_type="text/markdown",
    author="PolishBoiYT",
    author_email="polishboiyt@example.com",
    url="https://github.com/PolishBoiYT/PyTaskMGR",
    install_requires=[
        "psutil",
    ],
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent", 
    ],
    python_requires='>=3.6',
)
