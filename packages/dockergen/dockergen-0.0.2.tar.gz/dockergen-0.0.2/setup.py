import setuptools
import dockergen

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dockergen", # Replace with your own username
    version=dockergen.__version__,
    author="Janne Hellsten",
    author_email="jjhellst@gmail.com",
    description="Dockerfile generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nurpax/dockergen",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
