from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: MacOS',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='geometryMaths',
  version='0.0.1',
  description='A library made for making geometry in python simpler',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='The Goat',
  author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='geometry', 
  packages=find_packages(),
  install_requires=[''] 
)