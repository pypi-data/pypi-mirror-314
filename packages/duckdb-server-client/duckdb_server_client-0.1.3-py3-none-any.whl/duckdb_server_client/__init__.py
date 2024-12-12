"""
DuckDB HTTP客户端
提供简单的方式通过HTTP API与DuckDB服务器交互
"""

import requests
from typing import Optional, Any, Dict, Union
import json

class DuckDBClient:
    """DuckDB HTTP客户端类"""
    
    def __init__(self, host: str = "localhost", port: int = 9999, api_key: Optional[str] = None):
        """
        初始化DuckDB客户端
        
        Args:
            host: DuckDB服务器主机地址
            port: DuckDB服务器端口
            api_key: API密钥
        """
        self.base_url = f"http://{host}:{port}"
        self.api_key = api_key
        
    def execute(self, query: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数字典，用于参数化查询
            
        Returns:
            成功时返回查询结果字典
            失败时返回包含错误信息的字典，格式为：
            {
                "success": False,
                "error": "错误信息",
                "status_code": HTTP状态码
            }
        """
        headers = {}
        if self.api_key:
            headers["X-API-Key"] = self.api_key
            
        # 处理参数化查询
        if params:
            for key, value in params.items():
                placeholder = f":{key}"
                if isinstance(value, str):
                    # 字符串需要添加引号
                    query = query.replace(placeholder, f"'{value}'")
                else:
                    # 数字等其他类型直接替换
                    query = query.replace(placeholder, str(value))
            
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                data=query
            )
            
            # 检查响应状态
            if response.status_code != 200:
                return {
                    "success": False,
                    "error": response.text,
                    "status_code": response.status_code
                }
            
            # 尝试解析JSON响应
            try:
                return {
                    "success": True,
                    "data": response.json()
                }
            except json.JSONDecodeError:
                return {
                    "success": True,
                    "data": response.text
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": str(e),
                "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
            }

    def query(self, sql: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        执行SQL查询的便捷方法
        
        Args:
            sql: SQL查询语句
            params: 查询参数字典，用于参数化查询
            
        Returns:
            查询结果字典
        """
        return self.execute(sql, params) 