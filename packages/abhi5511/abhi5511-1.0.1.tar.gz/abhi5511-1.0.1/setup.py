from setuptools import setup, find_packages

setup(
    name="abhi5511",  
    version="1.0.1", 
    description="Ultra-secure, quantum-resistant hashing library by Abhi.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Abhishek Yadav",
    author_email="abbhishekyadav786@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=["pycryptodome"],  
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
