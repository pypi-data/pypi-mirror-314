from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="juryLLM",
    version="0.1.2",
    author="Sujith",
    description="An experimental framework for LLM discussions with judge oversight",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sujithhubpost/juryLLM",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=1.0.0",
        "ollama>=0.1.0",
        "pydantic>=2.0.0",
        "typing-extensions>=4.5.0",
        "aiohttp>=3.8.0",
        "asyncio>=3.4.3",
        "rich>=13.0.0"
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "black>=22.0",
            "isort>=5.0",
            "mypy>=0.9",
            "twine>=4.0.0",
            "build>=0.10.0"
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/juryLLM/issues",
        "Source": "https://github.com/yourusername/juryLLM",
        "Documentation": "https://github.com/yourusername/juryLLM/tree/main/docs"
    },
)
