from setuptools import setup, find_packages

setup(
    name="edgardsrs",
    version="0.1.1",  # Update this with your new version
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'lxml>=4.9.0'
    ],
    author="Pratik Relekar, Xinyao Qian",
    author_email="relekar2@illinois.edu, xinyaoq2@illinois.edu",
    description="A tool for cleaning SEC EDGAR HTML files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pratikrelekar/EdgarDSRS",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
