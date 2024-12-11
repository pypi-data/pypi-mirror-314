from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='foGLEb',
  version='0.0.1',
  description='A library that makes pygame developement a more easier and beginner friendly process.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Adam Yang',
  author_email='adam.fun.code@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='foGLEb', 
  packages=find_packages(),
  install_requires=['pygame>=2.6.0'] 
)