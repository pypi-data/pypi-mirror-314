from setuptools import setup, find_packages

setup(
    name="question-generator",
    version="0.1.2",
    author="David Schwartz",
    author_email="david.schwartz@devfactory.com",
    description="A CLI tool for generating prompts from Notion templates",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/devfactory/prompt-generator",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        'console_scripts': [
            'pg=cli.main:cli',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
