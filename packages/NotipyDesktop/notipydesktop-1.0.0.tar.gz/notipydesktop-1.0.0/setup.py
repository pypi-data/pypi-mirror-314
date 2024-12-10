from setuptools import setup, find_packages

setup(
    name="NotipyDesktop",  # Der Name des Pakets
    version="1.0.0",  # Versionsnummer
    description="A simple Python notification library using libnotify.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Michael Christian Dörflinger",
    author_email="michaeldoerflinger93@gmail.com",
    url="https://github.com/Michdo93/NotipyDesktop",
    packages=find_packages(),
    install_requires=[
        "PyGObject",  # Abhängigkeiten
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
