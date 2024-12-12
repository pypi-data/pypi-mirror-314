from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="WrappedLLM",
    version="0.1.9",
    packages=find_packages(),
    install_requires=[
        "openai",
        "anthropic",
        "google-generativeai",
        "pydantic",
    ],
    author="Jayam Gupta",
    author_email="guptajayam47@gmail.com",
    description="A wrapper for various large language models including GPT, Claude, and Gemini",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JayceeGupta/WrappedLLM",
    include_package_data=True,  # This ensures non-code files are included
    package_data={
    'WrappedLLM': ['README.md'],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)