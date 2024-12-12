from setuptools import setup, find_packages

setup(
    name="PipeX",
    version="0.1.01",
    author="Agnivesh Kumar",
    author_email="agniveshkumar15@gmail.com",
    description="The Data Pipeline Manager CLI is a command-line tool designed to automate and manage ETL (Extract, Transform, Load) workflows. These workflows are critical in data engineering for moving data from one system to another while applying transformations to make the data more useful.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pipex",  # Update with your actual URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.15.1",
        "pandas>=2.2.3",
        "SQLAlchemy>=2.0.36",
        "boto3>=1.35.74",
        "requests>=2.32.3",
        "pyyaml>=6.0.2",
        "tqdm>=4.67.1",
        "cachetools>=5.5.0",
        "python-dotenv>=1.0.1",
        "attrs>=24.2.0",
        "black>=24.10.0",
        "blinker>=1.9.0",
        "botocore>=1.35.76",
        "cleo>=2.1.0",
        "click>=8.1.7",
        "colorama>=0.4.6",
        "flask>=3.1.0",
        "pytest>=8.3.4",
        # Add other dependencies as per your `pyproject.toml`
    ],
    entry_points={
        "console_scripts": [
            "pipex=pipex:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
