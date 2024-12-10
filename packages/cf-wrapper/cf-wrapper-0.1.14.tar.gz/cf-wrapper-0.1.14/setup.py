from setuptools import setup, find_packages

setup(
    name="cf-wrapper",
    version="0.1.14",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "boto3>=1.26.0",
        "requests>=2.28.0",
        "python-dotenv>=0.19.0",
        "click>=8.0.0",
    ],
    entry_points={
        "console_scripts": [
            "cfw=cf_wrapper.cli:cli",
        ],
    },
)
