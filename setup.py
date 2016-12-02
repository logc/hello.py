"""
setup script for the hello package
"""
from setuptools import setup

setup(name='hello.py',
      version='0.1.0',
      packages=['hello'],
      entry_points={
          'console_scripts': [
              'hello = hello.main:run']})
