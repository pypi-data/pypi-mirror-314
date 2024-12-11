# 引入构建包信息的模块
from distutils.core import setup
import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

# 定义发布的包文件的信息
setup(
    name = "ss-datafeed",
    version = "1.1.2",
    description = "ss datafeed from ningbo,include some datasource",
    author = "kongshanxuelin",
    url = "http://www.sumscope.com",
    author_email = "33666490@qq.com",
    packages=setuptools.find_packages(),
    py_modules = ['__init__','ssdata','ssdata_util','ssdata_datasource']
)