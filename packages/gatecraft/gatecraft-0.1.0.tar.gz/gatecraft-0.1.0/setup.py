from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gatecraft",
    version="0.1.0",
    author="Lorenzo Abati",
    author_email="lorenzo.abati@glaider.it",
    description="A semantic RBAC system with RAG capabilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lorenzoabati/gatecraft",
    packages=find_packages(include=['gatecraft', 'gatecraft.*']),
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
    ],
    python_requires=">=3.8",
    install_requires=[
        "openai>=0.28.0",
        "pinecone-client>=2.2.1",
        "numpy>=1.21.0",
        "python-dotenv>=0.19.0",
    ],
) 