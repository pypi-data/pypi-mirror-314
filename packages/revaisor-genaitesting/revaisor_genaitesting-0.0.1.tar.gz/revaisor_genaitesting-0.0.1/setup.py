from setuptools import setup, find_packages

VERSION = '0.0.1' ## Lastest: PyPi 0.0.0, TestPyPi 0.0.12
DESCRIPTION = 'RevAIsor Python package for testing generative AI'
LONG_DESCRIPTION = """RevAIsor Python package for testing generative AI. 
This package provides a simple module for generating prompts to ask a generative AI and then evaluate the answers, to validate its behaviour."""

# Setting up
setup(
    name="revaisor_genaitesting", 
    version=VERSION,
    author="Felipe Henao",
    author_email="<felipe@revaisor.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",  # Add content type for long description
    packages=find_packages(),
    install_requires=[
        'requests',
        'tabulate',
        'pandas',
    ],  
    python_requires='>=3.6',  # Minimum Python version
    keywords=['python', 'generative AI', 'AI testing', 'machine learning'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ]
)