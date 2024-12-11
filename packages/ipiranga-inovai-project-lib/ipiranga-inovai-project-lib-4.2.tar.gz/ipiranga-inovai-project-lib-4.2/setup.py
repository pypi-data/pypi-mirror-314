from setuptools import setup, find_packages

setup(
    name="ipiranga-inovai-project-lib",
    version="4.2",
    packages=find_packages(),
    description="Projeto criado para importação genérica de entidades",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Clayton Sandes Monteiro",
    author_email="clayton.monteiro.ext@ipiranga.ipiranga",
    url="https://gitlab.ipirangacloud.com/clayton.monteiro.ext/ipiranga-inovai-project-lib",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="inovai",
)
