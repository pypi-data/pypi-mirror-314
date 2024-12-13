from setuptools import setup, find_packages

version = '0.0.2'

setup(
    name='wangph',
    version=version,
    description='wangph lib for 3d vision',
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/AuthorityWang/wangph',
    author='AuthorityWang',
    author_email='wangph1@shanghaitech.edu.cn',
    packages=find_packages()
)