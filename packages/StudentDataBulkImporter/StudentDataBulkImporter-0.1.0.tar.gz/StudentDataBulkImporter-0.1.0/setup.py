from setuptools import setup, find_packages

setup(
    name="StudentDataBulkImporter",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    description="SDK for importing and managing student data in bulk.",
    long_description_content_type="text/markdown",
    author="Rohan Dixit",
    author_email="rohan.dixit@samarth.ac.in",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
