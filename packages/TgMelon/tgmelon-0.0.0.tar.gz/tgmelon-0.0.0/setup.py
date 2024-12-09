from setuptools import setup, find_packages

setup(
    name="TgMelon",
    version="0.0.0",
    description="An advanced and comprehensive library for managing Telegram bots",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Ahmed Negm",
    author_email="a7mednegm.x@gmail.com",
    packages=find_packages(),
    install_requires=["flask", "urllib3"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)