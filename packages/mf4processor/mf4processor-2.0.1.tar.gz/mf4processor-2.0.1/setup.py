from setuptools import setup, find_packages

setup(
    name="mf4processor",
    version="2.0.1",
    description="A Python library for processing MF4 files",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Varshith V Hegde",
    author_email="varshithvh@gmail.com",
    url="https://github.com/varshithvhegde/mf4processor",  # Update with your repo link
    packages=find_packages(),
    install_requires=[
        "asammdf",
        "pandas",
        "numpy"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
