from setuptools import setup, find_packages

setup(
    name="analysis-of-prompts",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=2.1.0",
        "dask>=2023.12.0",
        "matplotlib>=3.8.0",
        "seaborn>=0.13.0",
        "plotly>=5.18.0",
        "networkx>=3.2.1",
        "streamlit>=1.29.0",
        "anthropic>=0.7.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pre-commit>=3.5.0",
            "ipdb>=0.13.0",
            "line-profiler>=4.1.1",
            "memory-profiler>=0.61.0",
            "sphinx>=7.1.0",
            "sphinx-rtd-theme>=1.3.0",
            "black>=23.12.0",
            "flake8>=6.1.0",
            "mypy>=1.7.0",
            "isort>=5.13.0",
            "apache-airflow>=2.7.0",
        ],
    },
    python_requires=">=3.8",
)
