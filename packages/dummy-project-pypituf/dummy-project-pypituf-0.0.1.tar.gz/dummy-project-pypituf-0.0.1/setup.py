from setuptools import setup, find_packages

setup(
    name="dummy-project-pypituf",
    version="0.0.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="A dummy project for testing PyPI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dummy_project",  # Optional
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
