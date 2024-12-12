from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="duckdb_server_client",
    version="0.1.3",
    author="lida",
    author_email="",  # 请填写您的邮箱
    description="DuckDB HTTP客户端，提供简单的方式通过HTTP API与DuckDB服务器交互",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lida/duckdb-server-py-client",  # 请修改为您的GitHub仓库地址
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
) 