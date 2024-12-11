
from setuptools import setup, find_packages
with open("README.md", "r") as fh: 
    long_description = fh.read() 

setup(
    name='createPackageTurner',
    version='0.2.21',
    author='Brigham Turner',
    author_email='brianbrandonturner@gmail.com',
    description='auto generated package from packageMaker',
    long_description=long_description, 
    long_description_content_type="text/markdown", 
    packages=find_packages(),
    install_requires=["pip","twine"], 
    license="MIT",
    classifiers=[
    'Programming Language :: Python :: 3',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)