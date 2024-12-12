import setuptools #导入setuptools打包工具
from setuptools import setup, find_packages

setuptools.setup(
    name="jcw_utils-yingyingguai", 
    version="0.10.5",   
    author="yingyingguai",   
    author_email="402117226@qq.com",    
    description="A small example package",
    # long_description=long_description,    #
    # long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",    #自己项目地址，比如github的项目地址
    packages=setuptools.find_packages(),
    # include_package_data=False,
    package_data={
        "": ["*.*"]
    },
    # classifiers=[
    #     "Programming Language :: Python :: 3.10",
    #     "Programming Language :: Python :: 3.12",
    #     "License :: OSI Approved :: MIT License",
    #     "Operating System :: OS Independent",
    #     "Development Status :: 5 - Production/Stable",
    #     "Intended Audience :: Developers",
    #     "Topic :: Software Development :: Libraries",
    # ],
    # python_requires='>=3.10',    #对python的最低版本要求
)