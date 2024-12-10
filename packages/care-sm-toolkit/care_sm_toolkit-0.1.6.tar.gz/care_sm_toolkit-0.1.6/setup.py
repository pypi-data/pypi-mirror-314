from setuptools import setup, find_packages

setup(
    name="care_sm_toolkit",  # Normalized project name to comply with PEP 625
    version="0.1.6",
    packages=find_packages(),
    author="Pablo Alarcón Moreno",
    author_email="pabloalarconmoreno@gmail.com",
    url="https://github.com/CARE-SM/CARE-SM-Toolkit",
    description="A toolkit for CARE-SM data transformation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords=["FAIR-in-a-box", "Fiab", "CARE-SM", "Toolkit", "EJP-RD", "ERDERA"],
    project_urls={
        "Source": "https://github.com/CARE-SM/CARE-SM-Toolkit",
        "Bug Tracker": "https://github.com/CARE-SM/CARE-SM-Toolkit/issues",
    },
)