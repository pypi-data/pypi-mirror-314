from setuptools import setup, find_packages

setup(
    name="betrand_ngoh_mutagha_version_12",  # Updated to reflect your project name
    version="0.2.0",  # Valid version string as per PEP 440
    author="BETRAND MUTAGHA",  # Replace with your name if needed
    author_email="mutagha2@gmail.com",  # Replace with your email
    url="https://github.com/Betrand1999/cicd",  # Updated with your repo URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "flask",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
)
