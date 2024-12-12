from setuptools import setup, find_packages
require_pakages = [
    'requests',
    'urllib3==1.26.15',
    'kssdutils==1.0.5'
]

setup(
    name='ssbpp',
    version='1.0.1',
    author='Hang Yang',
    author_email='yhlink1207@gmail.com',
    description="A Real-time Strain Submission and Monitoring Platform for Epidemic Prevention Based on Phylogenetic Placement ",
    url='https://github.com/yhlink/',
    download_url='https://pypi.org/project/ssbpp',
    py_modules=['ssbpp'],
    packages=find_packages(),
    install_requires=require_pakages,
    dependency_links=['https://pypi.python.org/simple/'],
    zip_safe=False,
    include_package_data=True
)
