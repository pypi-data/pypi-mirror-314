from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="prompt-enhancer",
    version="1.0.1",
    author="Moses-chris",
    author_email="moseschris535@gmail.com",
    description="An AI-powered prompt enhancement tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Moses-chris/terminal-prompt.git",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    install_requires=[
        "typer",
        "groq",
        "rich",
        "python-dotenv",
        "pyperclip",
        "prompt_toolkit"
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "isort",
            "flake8",
            "build",
            "twine",
        ],
    },
    entry_points={
        "console_scripts": [
            "prompt-enhancer=prompt_enhancer.cli:main",
        ],
    },
) 