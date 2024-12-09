# -*- coding: utf-8 -*-
from setuptools import find_packages, setup
from os import path as os_path
import time,datetime
# 获取当前日期
specific_date = datetime.date.today()
# print("当前日期：", current_date)
# 获取特定日期的年、月、日
year = specific_date.year
month = specific_date.month
day = specific_date.day
# 这里是基本的信息

name = 'django_tbase_post_product'  # 修改包名字-
version = f'{year}.{month}.{day}' + str(time.time())[:8]
description = 'Terry django base post ,'
author = 'Terry Chan'
author_email = 'napoler2008@gmail.com'
url = 'https://terrychanorg.jetbrains.space/p/django-expand/repositories/tbase_post_product/files/README.md'

copyright = '2021, Terry Chan'
language = 'zh_cn'

this_directory = os_path.abspath(os_path.dirname(__file__))
"""帮助[https://www.notion.so/6bade2c6a5f4479f82a4e67eafcebb3a]
上传到anaconda
https://docs.anaconda.com/anacondaorg/user-guide/tasks/work-with-packages/

    """


# 读取文件内容
def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


# 获取依赖
def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
            if not line.startswith('#')]


# long_description="""

# 这里是说明
# 一个创建库的demo
# http://www.terrychan.org/python_libs_demo/
# """


long_description = read_file("README.md")
setup(
    name=name,  # 修改包名字-
    version=version,
    description=description,
    author=author,
    author_email=author_email,
    url=url,
    # install_requires=read_requirements('requirements.txt'),  # 指定需要安装的依赖
    long_description=long_description,
    long_description_content_type="text/markdown",
    # 依赖文件
    install_requires=[
        'django-tbase-theme-tailwind>=2023.5.2116846028',
        'django-taggit==3.0.0',
        'martor==1.6.19'
        # 'sentence-splitter>=1.4',
        # 'requests>=2.28.1',
        # 'nltk>=3.7'
    ],
    packages=['tbase_post'],  # 扫描的目录
    include_package_data=True,  # 打包包含静态文件标识
)

"""
pip freeze > requirements.txt
python3 setup.py sdist
#python3 setup.py install
python3 setup.py sdist upload
"""