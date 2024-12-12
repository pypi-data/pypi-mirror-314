from setuptools import setup, find_packages

setup(
    name="md_caba",
    version="0.1.1",
    packages=find_packages(),
    install_requires=[
        "markdown>=3.3.0",
    ],
    author="CaBa52052",
    author_email="CaBa52052@qq.com",
    description="一个简单的Markdown文件读取和解析工具",
    long_description=open("README.md", encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/CaBa52052/md_caba",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
) 