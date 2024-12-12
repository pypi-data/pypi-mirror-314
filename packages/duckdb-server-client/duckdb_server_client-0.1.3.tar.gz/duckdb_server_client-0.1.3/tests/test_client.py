import unittest
from unittest.mock import patch, MagicMock
from duckdb_server_client import DuckDBClient

class TestDuckDBClient(unittest.TestCase):
    """DuckDBClient测试类"""

    def setUp(self):
        """测试前的设置"""
        self.client = DuckDBClient(api_key="user:pass")

    def test_init(self):
        """测试初始化"""
        client = DuckDBClient(host="192.168.31.203", port=9999, api_key="user:pass")
        self.assertEqual(client.base_url, "http://192.168.31.203:9999")
        self.assertEqual(client.api_key, "user:pass")

    @patch('requests.post')
    def test_execute_success(self, mock_post):
        """测试成功执行查询"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": [{"id": 1}]}
        mock_post.return_value = mock_response

        result = self.client.execute("SELECT VERSION();")
        
        # 验证结果
        self.assertEqual(result, {"result": [{"id": 1}]})
        
        # 验证请求参数
        mock_post.assert_called_once_with(
            "http://192.168.31.203:9999",
            headers={"X-API-Key": "user:pass"},
            data="SELECT * FROM test"
        )

    @patch('requests.post')
    def test_execute_non_json_response(self, mock_post):
        """测试非JSON响应"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.side_effect = ValueError
        mock_response.text = "非JSON响应"
        mock_post.return_value = mock_response

        result = self.client.execute("SELECT * FROM test")
        self.assertEqual(result, {"response": "非JSON响应"})

    @patch('requests.post')
    def test_query_method(self, mock_post):
        """测试query方法"""
        # 模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": [{"id": 1}]}
        mock_post.return_value = mock_response

        result = self.client.query("SELECT * FROM test")
        self.assertEqual(result, {"result": [{"id": 1}]})

if __name__ == '__main__':
    unittest.main() 