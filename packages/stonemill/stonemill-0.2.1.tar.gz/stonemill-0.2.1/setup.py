from setuptools import setup, find_packages
import os

setup(
   name='stonemill',
   version='0.2.1',
   packages=find_packages(),
   install_requires=[],
   entry_points={
       'console_scripts': [
           'stonemill=stonemill.stonemill:main',
       ],
   },
   # Metadata
   author='Mirror12k',
   description='A terraform scaffolding tool',
   long_description=open('README.md').read(),
   long_description_content_type='text/markdown',
   license='MIT',
   keywords='aws terraform scaffolding',
   url='https://github.com/mirror12k/stonemill',
   include_package_data=True,
   classifiers=[
       'Programming Language :: Python :: 3',
       'License :: OSI Approved :: MIT License',
   ],
)
