from setuptools import setup, find_packages

setup(
    name="quickqr",  # Package name
    version="0.3.0",  # Version number
    packages=find_packages(),
    install_requires=[
        "qrcode[pil]",
        "Pillow",
    ],
    description="A QR Code Generator with customizable options, very easy to use. It very quick too",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TheSpaceDEVe",
    url="https://github.com/sonexeee/QuickQR",  # Your GitHub repository link
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
