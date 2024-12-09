from setuptools import setup, find_packages

setup(
    name="search-prompts",
    version="1.2.0",
    description="A library for efficient text-based prompt search with resource monitoring.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Kozlovskiy Sergei",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "memory_profiler",
        "datasets",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
