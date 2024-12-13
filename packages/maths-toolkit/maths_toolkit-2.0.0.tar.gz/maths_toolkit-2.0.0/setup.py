from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="maths-toolkit",
    version="2.0.0",
    author="N V R K Sai Kamesh Sharma",
    author_email="your-email@example.com",
    description="A toolkit for intermediate-level Maths A and Maths B calculations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Kalasaikamesh944/maths-toolkit",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)