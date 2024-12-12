# coding=utf-8
from setuptools import setup, find_packages

setup(
    name='shangyi-big_math',
    version='0.1',
    packages=find_packages(),
    description='A simple example package',
    # python3，readme文件中文报错
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='',
    author='shangyi',
    author_email='',
    license='MIT',
    install_requires=[
        # 依赖列表
    ],
    classifiers=[
        # 分类信息
    ]
)
