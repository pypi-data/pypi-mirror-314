# DuckDB Server Python Client

这是一个用于与DuckDB HTTP服务器交互的Python客户端库。它提供了一个简单的接口来执行SQL查询并获取结果。

## 安装

```bash
pip install duckdb-server-py-client
```

## 使用示例

```python
from duckdb_client import DuckDBClient

# 创建客户端实例
client = DuckDBClient(host="localhost", port=9999)

# 执行查询
result = client.query("SELECT * FROM my_table")

# 检查查询是否成功
if result["success"]:
    print(result["data"])
else:
    print(f"查询失败: {result['error']}")
```
378b8a1092423ff1
## 特性

- 简单易用的API
- 支持API密钥认证
- 自动处理HTTP请求和响应
- 完善的错误处理

## API文档

### DuckDBClient

#### 初始化

```python
client = DuckDBClient(host="localhost", port=9999, api_key=None)
```

参数:
- host: DuckDB服务器主机地址
- port: DuckDB服务器端口
- api_key: API密钥（可选）

#### 方法

##### execute(query: str)
执行SQL查询并返回结果。

##### query(sql: str)
execute方法的别名，用于执行SQL查询。

## 许可证

MIT License
