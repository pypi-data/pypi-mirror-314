from setuptools import setup, find_packages

setup(
    name='quickqr',  # Name of the package
    version='0.1.0',  # Initial version
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[  # List of dependencies required for the package to run
        'qrcode[pil]',  # QR Code generation library
        'Pillow',        # Python Imaging Library (used for saving QR code images)
    ],
    description='A simple Python module for generating QR codes from URLs, text, and images.',
    long_description=open('README.md').read(),  # Read long description from the README file
    long_description_content_type='text/markdown',  # Markdown for long description
    author='SpaceDEV',  # Your name (or your company's name)
    url='https://github.com/sonexeee/QuickQR/tree/main',  # URL to the project (e.g., GitHub repository)
    classifiers=[  # Classification for PyPI to help users find the package
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Minimum Python version required
)
