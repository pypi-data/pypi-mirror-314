from setuptools import setup, find_packages

setup(
    name="redactCREW",
    version="1.0.0",
    author="redactcrew",
    author_email="rmdvcbe9@gmail.com",
    description="A package for PII redaction, encryption, and OCR workflows.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhayeah7/redactCREW",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=open("requirements.txt").read().splitlines(),
)
