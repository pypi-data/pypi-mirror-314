from setuptools import setup, find_packages

setup(
    name="goliath-llm-client",  # Changed name to be unique on PyPI
    version="0.1.1",  # Increment version number
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "PyYAML>=5.1",
        "urllib3>=1.26.0"
    ],
    author="Goliath Team",
    author_email="your.email@example.com",
    description="A Python client library for the Goliath LLM API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/goliath-client",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    include_package_data=True,
    package_data={
        'goliath_client': ['list_models.yaml'],
    },
)
