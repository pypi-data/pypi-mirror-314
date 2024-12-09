# setup.py

from setuptools import setup, find_packages

setup(
    name="davidsousa",
    version="0.3.0",
    packages=find_packages(),
    description="Biblioteca para envio de e-mails com suporte a HTML e prioridade (Experimental). (Gmail)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="David Sousa",
    author_email="davidffsousaff@gmail.com",
    url="https://github.com/davidsousadev/davidsousa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="email gmail smtp sending",  
    python_requires='>=3.6',
    install_requires=[
        "secure-smtplib",
    ],
    include_package_data=True, 
    zip_safe=False,  
)
