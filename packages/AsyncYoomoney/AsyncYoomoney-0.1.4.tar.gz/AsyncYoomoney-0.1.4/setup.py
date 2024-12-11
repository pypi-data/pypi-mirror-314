from setuptools import setup, find_packages, Extension

setup(
    name='AsyncYoomoney',
    version='0.1.4',
    packages=find_packages(exclude=['tests']),
    url='https://github.com/vxjnc/async-yoomoney-api.git',
    license='GPL-3.0',
    author='vxjnc',
    author_email='vxjnc0@gmail.com',
    description='Unofficial YooMoney API python library',
    long_description=str(open('README.rst').read())
)
