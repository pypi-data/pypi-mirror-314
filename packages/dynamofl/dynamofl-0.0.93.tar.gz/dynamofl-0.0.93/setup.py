"""
Defines the Python package setup for the dynamofl package.
"""
from setuptools import find_namespace_packages, setup

setup(
    name="dynamofl",
    version="0.0.93",
    author="Emile Indik",
    long_description="DynamoFL Core Python Client",
    long_description_content_type="text/markdown",
    packages=find_namespace_packages(),
    python_requires=">=3.7",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "requests==2.31.0",
        "websocket-client==1.5.0",
        "shortuuid==1.0.11",
        "tqdm==4.66.1",
        "dataclasses-json==0.6.7",
    ],
)
