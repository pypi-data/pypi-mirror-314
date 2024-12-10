from setuptools import setup, find_packages

setup(
    name="rich-text-package",
    version="0.0.1",
    packages=find_packages(),
    include_package_data=True,
    description="Un package Django pour gérer du texte riche.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.com/webissito/widgets/",
    author="Alexandre PEPIN",
    author_email="alexandre.pepin@webissito.fr",
    license="MIT",
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
