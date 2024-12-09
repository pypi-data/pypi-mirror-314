from setuptools import setup, find_packages

setup(
    name="augmenter",
    version="0.1.0",
    description="A toolkit for automated data augmentation",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="AKM Korishee Apurbo",
    author_email="bandinvisible8@gmail.com",
    url="https://github.com/IMApurbo/augmenter",
    packages=find_packages(),
    install_requires=[
        "opencv-python",
        "albumentations",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
