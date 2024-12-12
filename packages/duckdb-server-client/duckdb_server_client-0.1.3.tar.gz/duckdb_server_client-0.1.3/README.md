# DuckDB Server Python Client

这是一个简单的Python客户端库，用于通过HTTP API与DuckDB服务器进行交互。

## 安装

```bash
pip install duckdb-server-client
```

## 使用方法

### 基本使用

```python
from duckdb_server_client import DuckDBClient

# 创建客户端实例
client = DuckDBClient(
    host="localhost",  # 默认值
    port=9999,        # 默认值
    api_key=None      # 可选的API密钥
)

# 执行简单查询
result = client.execute("SELECT * FROM users")
if result["success"]:
    print(result["data"])
else:
    print(f"错误: {result['error']}")
```

### 参数化查询

支持使用命名参数进行参数化查询：

```python
# 使用参数化查询
result = client.execute(
    "SELECT * FROM users WHERE age > :min_age AND city = :city",
    {
        "min_age": 18,
        "city": "北京"
    }
)

# 等同于执行：SELECT * FROM users WHERE age > 18 AND city = '北京'
```

### 返回值格式

成功时返回：
```python
{
    "success": True,
    "data": <查询结果>  # JSON数据或文本
}
```

失败时返回：
```python
{
    "success": False,
    "error": "错误信息",
    "status_code": HTTP状态码
}
```

## 特性

- 简单易用的API
- 支持参数化查询
- 支持API密钥认证
- 自动处理JSON响应
- 完善的错误处理

## 注意事项

- 参数化查询中的参数名需要使用`:`作为前缀
- 字符串类型的参数会自动添加单引号
- 数字类型的参数会直接替换到SQL语句中

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
