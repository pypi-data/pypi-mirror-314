from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sibra_logger",
    version="1.0.0",
    description="Configurable logging for Python applications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ashraf Inamdar",
    author_email="ashrafinamdar@gmail.com",
    url="https://github.com/primabonito/sibralogger",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "sibra_logger": ["log_config.yaml"],  # Ensure YAML config is included
    },
    install_requires=[
        "pyyaml>=5.4.1",  # YAML configuration support
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.5", 
            "pytest-mock>=3.6.1", 
            "twine>=4.0.0"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="logging python configurable logging yaml configuration",
    python_requires=">=3.6",
    license="MIT",
)