from setuptools import setup, find_packages

setup(
    name="goliath-client",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0"
    ],
    author="Goliath Team",
    description="A Python client library for the Goliath LLM API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)
