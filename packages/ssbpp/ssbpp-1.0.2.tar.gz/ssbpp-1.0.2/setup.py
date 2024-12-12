from setuptools import setup, find_packages

VERSION = '1.0.2'
require_pakages = [
    'requests',
    'kssdutils'
]
setup(name='ssbpp',
      version=VERSION,
      description="A Real-time Strain Submission and Monitoring Platform for Epidemic Prevention Based on Phylogenetic Placement ",
      classifiers=[],
      keywords='ssbpp',
      author='Hang Yang',
      author_email='1090692248@qq.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=True,
      install_requires=require_pakages,
      entry_points={
          'console_scripts': [
              'ssbpp = ssbpp.case:main'
          ]
      }
      )
