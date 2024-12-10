from setuptools import setup, find_packages
import shutil

shutil.rmtree('dist', ignore_errors=True)
shutil.rmtree('build', ignore_errors=True)
shutil.rmtree('TeleClient.egg-info', ignore_errors=True)

setup(
    name = "telethon-client",
    version = "0.1.9",
    packages = find_packages(),
    install_requires = ["Telethon>=1.35.0", "requests>=2.32.3"],
    author= " LEGENDX",
    author_email = "legendxcoder@gmail.com",
    description = "Custom Telethon Client for My Usage",
    long_description = open('README.md').read(),
    long_description_content_type = "text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)