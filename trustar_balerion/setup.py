from setuptools import setup, find_packages

setup(name='trustar_balerion',
      version='0.0.1',
      author='TruSTAR Technology Inc.',
      url='https://github.com/trustar_balerion/trustar_balerion-balerion',
      description='Python SDK for TruSTAR Balerion Tools',
      author_email='nkseib@trustar_balerion.co',
      license='Apache',
      packages=find_packages(),
      use_2to3=True, requires=['py2neo', 'pandas']
      )