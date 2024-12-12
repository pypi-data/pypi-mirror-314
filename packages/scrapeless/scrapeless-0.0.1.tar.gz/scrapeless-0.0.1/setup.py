import os
from setuptools import setup

VERSION = "0.0.1"


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="scrapeless",
    version=VERSION,
    author="scrapelessteam",
    author_email="scrapelessteam@gmail.com",
    description="scrapeless python sdk",
    license="MIT",
    keywords=[
        "scrapeless",
        "browserless",
        "scraping browser",
        "scraping",
        "web unlocker",
        "captcha solver",
        "rotate proxy"
    ],
    url="https://github.com/scrapeless-ai/scrapeless-sdk-python",
    project_urls={
        "Documentation": "https://github.com/scrapeless-ai/scrapeless-sdk-python#readme",
        "Source": "https://github.com/scrapeless-ai/scrapeless-sdk-python",
    },
    packages=["scrapeless"],
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    install_requires=["requests"],
)
