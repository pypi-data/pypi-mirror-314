from datetime import datetime
from setuptools import setup, find_packages

# 读取文件内容
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
# python setup.py sdist
# twine upload dist/*
# 获取当前日期和时间
now = datetime.now()
today = now.date()

setup(
    name="qtmodel",
    version="0.5.44",
    author="dqy-zhj",
    author_email="1105417715@qq.com",
    description=f"python modeling for qt {today} ",
    long_description=long_description,  # 使用读取的 README.md 文件内容
    long_description_content_type="text/markdown",  # 指明内容格式为markdown
    url="https://github.com/Inface0443/pyqt",
    packages=find_packages(),
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: OS Independent",
    ],
)

