from setuptools import setup, find_packages

setup(
    name="hoaipham_lib",  # Replace with your package name
    version="0.1.0",  # Version of your package
    author="Hoai Pham",
    author_email="hoaipham2501@gmail.com",
    description="A sample Python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
