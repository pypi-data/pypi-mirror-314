from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="Swarm-Plus",
    version="0.0.8",
    description=("""Swarm-Plus is a Python framework developed by Vishnu Durairaj. for developing AI agents equipped with specialized roles and tools to handle complex user requests efficiently."""
    ),

    long_description=long_description,
    long_description_content_type="text/markdown",
    readme = "README.md",
    author="Vishnu.D",
    author_email="",
    license="MIT",
    keywords =["pip install Swarm-Plus","pip install Swarm Plus", "Swarm-Plus", "AI Agent Framework Swarm-Plus", "Multi Agent Framework"],
    packages=find_packages(),
    install_requires=[
            # Required Packages
            "openai==1.40.1",
            "anthropic==0.34.1",
            "pandas==2.2.2",
            "pydantic==2.8.2",
            "pybase64==1.4.0",
            "requests==2.32.3",
            "tiktoken==0.7.0",
            "chainlit==1.3.1",
            "websocket-client==1.8.0",
            "lxml==5.3.0",
            "notebook==7.2.1",
            "groq==0.11.0",
            "httpx==0.27.2",
            "chromadb==0.5.11",
            "sentence-transformers==3.1.1",
            "marshmallow==3.23.1"
        ],


    classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.12',
  ]
)