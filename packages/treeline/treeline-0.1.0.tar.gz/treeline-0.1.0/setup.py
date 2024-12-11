from setuptools import find_packages, setup

setup(
    name="treeline",
    version="0.1.0",
    packages=find_packages(),
    package_data={
        "treeline": ["default_ignore"],
    },
    description="A simple code analysis tool for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown", 
    author="oha",
    author_email="aaronoh2015@gmail.com",
    url="https://github.com/duriantaco/treeline",
    license="MIT",
    entry_points={
        "console_scripts": [
            "treeline=treeline.core:main",
        ],
    },
    python_requires=">=3.7",
    extras_require={
        "dev": [
            "pre-commit>=2.21.0",
            "black>=24.2.0",
            "isort>=5.13.2",
            "pytest>=7.0.0",
            "black[jupyter]",
        ],
    },
)
