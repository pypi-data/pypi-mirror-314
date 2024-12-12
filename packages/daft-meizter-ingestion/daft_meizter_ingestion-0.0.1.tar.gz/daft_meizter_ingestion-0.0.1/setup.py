from setuptools import setup, find_packages

# Lê as dependências de requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name="daft_meizter_ingestion",
    version="0.0.1",
    author="Douglas B. Martins",
    author_email="douglas@meizter.com",
    description="lakehouse with daft",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)