from setuptools import setup, find_packages

setup(
    name="python-bitget-api",  
    version="3.3.5",  
    packages=["pybitgetapi"],
    description="bitget python wrapper with rest API, websocket API.",
    long_description=open("README.md").read(),
    url="https://github.com/cuongitl/python-bitget",
    author="Cuongitl",
    author_email='mrcuongit@live.com',
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
