import unittest
from duckdb_server_client import DuckDBClient
import os

class TestDuckDBClientIntegration(unittest.TestCase):
    """DuckDBClient集成测试"""

    @classmethod
    def setUpClass(cls):
        """设置测试环境"""
        # 从环境变量获取配置，如果没有则使用默认值
        cls.host = os.getenv("DUCKDB_HOST", "localhost")
        cls.port = int(os.getenv("DUCKDB_PORT", "9999"))
        cls.api_key = os.getenv("DUCKDB_API_KEY", "secretkey")
        
        cls.client = DuckDBClient(
            host=cls.host,
            port=cls.port,
            api_key=cls.api_key
        )

    def test_simple_query(self):
        """测试简单查询"""
        try:
            result = self.client.query("SELECT 1 as number")
            self.assertIn("result", result)
        except Exception as e:
            self.fail(f"查询失败: {str(e)}")

    def test_complex_query(self):
        """测试复杂查询"""
        try:
            result = self.client.query("LOAD chsql; SELECT *, uuid() FROM numbers(5)")
            self.assertIn("result", result)
        except Exception as e:
            self.fail(f"复杂查询失败: {str(e)}")

if __name__ == '__main__':
    unittest.main() 