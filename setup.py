from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A Python wrapper for Temp Mail API.'

setup(
    name="temp-mail-python",
    version=VERSION,
    author="Anhy Krishna Fitiavana",
    author_email="fitiavana.krishna@gmail.com",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ]
)
