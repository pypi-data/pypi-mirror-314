from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='deepakGPAconversion',
  version='0.0.3',
  description='A basic GPA to Percentage convertor',
  url='',  
  author='Deepak Tyagi',
  author_email='X23178019@student.ncirl.ie',
  license='MIT', 
  classifiers=classifiers,
  keywords='convertor', 
  packages=find_packages(),
  install_requires=[''] 
)