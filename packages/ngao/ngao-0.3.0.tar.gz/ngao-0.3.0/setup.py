from setuptools import setup, find_packages

setup(
    name="ngao",
    version="0.3.0",
    packages=find_packages(),
    install_requires=[
        "ngiri",  # Required for HTTP requests to external APIs
    ],
    entry_points={
        "console_scripts": [
            "ngao=ngao.cli:main",
        ],
    },
    author="Mark Francis / Masasi Mgengeli ",
    author_email="support@ngao.pro",
    description="NGAO - Tunnel local ports to public URLs and inspect traffic",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ngao",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
