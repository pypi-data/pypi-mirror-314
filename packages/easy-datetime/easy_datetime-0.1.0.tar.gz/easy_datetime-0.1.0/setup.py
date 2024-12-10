from setuptools import setup, find_packages

setup(
    name="easy_datetime",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "python-dateutil>=2.8.2",
    ],
    author="Lucy",
    author_email="",
    description="A package to automatically detect and convert datetime strings to Unix timestamps",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/easy_datetime",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
