from setuptools import setup, find_packages

setup(
    name="pyonix",
    version="0.1.0",
    description="A Python client library for the Ionix API",
    author="Josiah",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.4",
        "requests>=2.32.3",
    ],
    extras_require={
        'test': [
            'unittest-mock>=1.3.0',
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
