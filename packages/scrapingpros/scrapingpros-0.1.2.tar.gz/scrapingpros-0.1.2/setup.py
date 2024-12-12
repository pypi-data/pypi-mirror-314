from setuptools import setup, find_packages

setup(
    name="scrapingpros",  
    version="0.1.2",      #  Initial version: 0.1.0
    author="Scraping Pros",
    author_email="team@scrapingpros.com",
    description="Scraping Pros API Client",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/7Puentes/batua2/sprosdata-python",  # Repo URL
    packages=find_packages(),
    install_requires=["requests"],  # Dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
