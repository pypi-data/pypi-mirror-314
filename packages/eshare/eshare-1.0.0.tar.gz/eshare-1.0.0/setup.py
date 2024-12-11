from setuptools import setup, find_packages

setup(
    name="eshare",
    version="1.0.0",
    description="Encrypted File Sharing Command-Line Tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Parth Dudhatra",
    author_email="imparth.dev@gmail.com",
    url="https://github.com/imparth7/eshare",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "cryptography==41.0.0",
        "typer==0.9.0",
        "bcrypt==4.0.1",
    ],
    entry_points={
        "console_scripts": [
            "eshare=eshare.app:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="encryption, file-sharing, cli, secure, python, password, cryptography",
    platforms="Any",
)
