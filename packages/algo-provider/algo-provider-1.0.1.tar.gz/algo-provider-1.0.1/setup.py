from setuptools import setup, find_packages
from algo_provider.app import APP_VERSION

# Import the README and use it as the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Setup the package
setup(
    name="algo-provider",
    version=APP_VERSION,
    description="Start your own Algo provider from a Python function,\
 interface it DebiAI or something else",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/debiai/eaty-algo-provider",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "fastapi==0.115.4",
        "uvicorn==0.32.0",
        "rich==13.9.4",
    ],
    entry_points={},
)
