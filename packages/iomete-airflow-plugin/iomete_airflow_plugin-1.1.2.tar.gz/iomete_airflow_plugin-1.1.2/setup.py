#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md") as readme_file:
    readme = readme_file.read()

setup(
    author="IOMETE",
    author_email="support@iomete.com",
    python_requires=">=3.8",
    description="An Airflow plugin for interacting with IOMETE platform.",
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    license="Apache Software License 2.0",
    long_description=readme,
    long_description_content_type="text/markdown",
    include_package_data=True,
    name="iomete_airflow_plugin",
    url="https://github.com/iomete/iomete-airflow-plugin",
    version="1.1.2",
    packages=find_packages(
        include=["iomete_airflow_plugin", "iomete_airflow_plugin.*"]
    ),
    entry_points={
        "airflow.plugins": [
            "iomete = iomete_airflow_plugin.plugin:IometePlugin"
        ]
    },
    keywords=['iomete', 'airflow', 'airflow plugin'],
    extras_require={
        'dev': ['black==24.10.0', 'watchdog==6.0.0', 'twine==6.0.1', 'apache-airflow==2.10.3']
    },
    install_requires=[
        "requests==2.32.3",
        "setuptools==75.6.0",
        "Flask==2.2.5",
        "iomete-sdk==2.1.2",
    ],
)
