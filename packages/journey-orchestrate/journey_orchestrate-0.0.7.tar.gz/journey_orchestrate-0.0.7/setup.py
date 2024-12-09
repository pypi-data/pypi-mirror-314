from setuptools import setup, find_packages
with open("README.md","r") as f:
    descrip = f.read()
setup(
name='journey_orchestrate',
version='0.0.7',
author='Dhivya Nagasubramanian',
author_email='nagas021@alumni.umn.edu',
description='Customer Journey Orchestration Utility',
packages=find_packages(),
classifiers=[
'Programming Language :: Python :: 3',
'License :: OSI Approved :: MIT License',
'Operating System :: OS Independent',
],
python_requires='>=3.6',
long_description = descrip,
long_description_content_type='text/markdown',
)