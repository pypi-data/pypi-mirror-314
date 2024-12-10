from setuptools import setup, find_packages

setup(
    name="ckey",
    version="1.0.0a1",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.0.0",
        "requests>=2.31.0",
        "ThreadPoolExecutorPlus>=0.2.2"
    ],
    author="Justin G. Davis",
    description="OpenFEC API client for researching the political spending of executives",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/justin-g-davis/ckey",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
