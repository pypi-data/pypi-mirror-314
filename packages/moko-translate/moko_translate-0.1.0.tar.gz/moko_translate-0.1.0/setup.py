from setuptools import setup, find_packages

setup(
    name="moko_translate",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers"
    ],
    description="A translation package using Sunbird's NLLB model.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Bateesa Saul Tobius",
    author_email="tobiusaolo21@gmail.com",
    url="https://github.com/your_username/translate_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

