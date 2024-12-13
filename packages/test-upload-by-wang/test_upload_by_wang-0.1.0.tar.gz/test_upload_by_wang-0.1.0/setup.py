from setuptools import setup, find_packages

setup(
    name="test_upload_by_wang",              # 包的名称
    version="0.1.0",                       # 包的版本号
    author="Wang Hui",                    # 作者
    author_email="12210332@mail.sustech.edu.cn", # 作者邮箱
    description="A simple example package for PyPI",  # 简短描述
    long_description=open("README.md").read(),        # 详细描述
    long_description_content_type="text/markdown",    # 描述文件的格式
    url="https://github.com/your_username/my_simple_package", # 项目主页链接
    packages=find_packages(),              # 自动发现包
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",               # Python 版本要求
)
