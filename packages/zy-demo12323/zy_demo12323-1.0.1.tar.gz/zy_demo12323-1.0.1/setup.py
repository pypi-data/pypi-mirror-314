import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zy_demo12323", # 模块名称
    version = "1.0.1", # 当前版本
    author="zhengyu", # 作者
    author_email="543278005@qq.com", # 作者邮箱
    description="simple demo package", # 简短介绍
    long_description=long_description, # 模块详细介绍
    long_description_content_type="text/markdown", # 模块详细介绍格式
    packages=setuptools.find_packages(), # 自动找到项目中导入的模块
    # 模块相关的元数据(更多描述信息)
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    # 依赖模块
    install_requires=[
        'numpy'
    ],
    python_requires=">=3",
    # url="https://github.com/UncoDong", # github地址
)

