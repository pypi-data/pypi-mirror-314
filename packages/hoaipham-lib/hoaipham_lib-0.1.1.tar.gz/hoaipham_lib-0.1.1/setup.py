import os
from setuptools import setup, find_packages
here = os.path.abspath(os.path.dirname(__file__))

# Read requirements.txt safely
requirements_path = "/Users/hoai.pham/Desktop/hoaipham_package/requirements.txt"
# if os.path.isfile(requirements_path):

# else:
#     requirements = []

with open(requirements_path) as f:
    requirements = f.read().splitlines()

    setup(
        name="hoaipham_lib",  # Replace with your package name
        version="0.1.1",  # Version of your package
        author="Hoai Pham",
        author_email="hoaipham2501@gmail.com",
        description="A sample Python package",
        long_description=open("README.md").read(),
        long_description_content_type="text/markdown",
        packages=find_packages(),
            entry_points={
            "console_scripts": [
                "hoaipham_lib-cli=hoaipham_lib.mymodule:main",  # Link `mypackage-cli` to `main` in `mymodule.py`
            ]
        },
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
        install_requires=requirements,
    )
