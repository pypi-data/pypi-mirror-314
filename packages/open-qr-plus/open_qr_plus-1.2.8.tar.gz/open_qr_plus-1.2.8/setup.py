from setuptools import setup, find_packages

setup(
    name="open_qr_plus",  # Name of your project
    version="1.2.8",  # Initial version
    author="Sandesh Kumar",
    author_email="connect@sandeshai.in",
    description="A perfect solution for qr generation with stunning ui...",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'open-qr-plus=open_qr_plus.server:start',  # This allows running `open-qr` from the command line
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_data={ '': ['templates/*'], 
                   },
    python_requires=">=3.10",  # Minimum Python version
    install_requires=open("requirements.txt").readlines(),  # Dependencies
)

