import setuptools  # 导入setuptools打包工具

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="crawltwj",  # 用自己的名替换其中的YOUR_USERNAME_
    version="0.0.8",  # 包版本号，便于维护版本
    author="twj",  # 作者，可以写自己的姓名
    description="this is a crawl process",  # 包的简述
    long_description=long_description,  # 包的详细介绍，一般在README.md文件内
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires='>=3.6',  # 对python的最低版本要求
)