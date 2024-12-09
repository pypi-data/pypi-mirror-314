from setuptools import setup, find_packages

setup(
    name="hexgpc",      version="1.1.0",  
    description="A Package that Converts Images & Videos into Binary, Reads the Binary pixels converts the Pixels into hexadecimal Values.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  
    author="Byt3signal",
    author_email="hexgpcauthor@gmail.com",
    url="https://pypi.org/project/hexgpc/",  
    packages=find_packages(),  # Automatically finds all sub-packages
    install_requires=["Pillow"],  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  
)
