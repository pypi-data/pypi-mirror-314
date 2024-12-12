from setuptools import setup, find_packages

setup(
    name="aiq_insights",  # The name of your package
    version="0.1.0",  # Your first version
    description="A Python library for checking common errors in multiple-choice questions (MCQs)",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="doctsh@gmail.com",
    url="https://github.com/Shiva-DS24/aiq_insights",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Adjust if using a different license
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "transformers>=4.0.0",  # Required for transformers package
        "scipy>=1.5.0",         # Required for scipy (cosine similarity)
        "torch>=1.9.0",         # Required for PyTorch
    ],
    python_requires='>=3.6',  # Adjust based on your target Python version
)