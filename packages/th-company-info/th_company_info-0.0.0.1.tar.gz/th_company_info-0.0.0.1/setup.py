from setuptools import setup, find_packages

setup(
    name="th-company-info",
    version="0.0.0.1",
    description="A Python library to get a company information from dataforthai.com (For my eductaional purpose)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Grassroot Engineer",
    author_email="q_electronics@hotmail.com",
    # url="https://github.com/atthana/th-company-info",
    packages=find_packages(),
    install_requires=[
        "cloudscraper",
        "beautifulsoup4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
