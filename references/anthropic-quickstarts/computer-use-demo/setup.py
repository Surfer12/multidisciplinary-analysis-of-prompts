from setuptools import find_packages, setup

setup(
    name="computer_use_demo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "anthropic>=0.42.0",
        "prometheus-client>=0.19.0",
        "asyncio>=3.4.3",
    ],
    python_requires=">=3.9",
)
