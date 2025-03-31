import pytest
import json
from unittest.mock import patch, MagicMock
from client.book_client import BookClient

class TestBookClient:
    """测试BookClient类"""
    
    def setup_method(self):
        """每个测试方法运行前的设置"""
        self.base_url = "http://localhost:8000"
        self.client = BookClient(self.base_url)
        
        # 测试数据
        self.test_book = {
            "id": 1,
            "title": "测试书籍",
            "author": "测试作者",
            "publication_year": 2022,
            "isbn": "1234567890"
        }
        
        self.test_books = [
            self.test_book,
            {
                "id": 2,
                "title": "另一本书",
                "author": "另一个作者",
                "publication_year": 2021,
                "isbn": "9876543210"
            }
        ]
    
    @patch('client.book_client.requests.get')
    def test_get_all_books_success(self, mock_get):
        """测试成功获取所有书籍"""
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": self.test_books}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 调用客户端方法
        books, error = self.client.get_all_books()
        
        # 验证结果
        assert error is None
        assert books == self.test_books
        mock_get.assert_called_once_with(f"{self.base_url}/books")
    
    @patch('client.book_client.requests.get')
    def test_get_all_books_error(self, mock_get):
        """测试获取所有书籍时出错"""
        # 配置模拟响应
        mock_get.side_effect = Exception("模拟的网络错误")
        
        # 调用客户端方法
        books, error = self.client.get_all_books()
        
        # 验证结果
        assert books is None
        assert error is not None
        assert "模拟的网络错误" in error
    
    @patch('client.book_client.requests.get')
    def test_get_book_success(self, mock_get):
        """测试成功获取单本书籍"""
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": self.test_book}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # 调用客户端方法
        book, error = self.client.get_book(1)
        
        # 验证结果
        assert error is None
        assert book == self.test_book
        mock_get.assert_called_once_with(f"{self.base_url}/books/1")
    
    @patch('client.book_client.requests.get')
    def test_get_book_error(self, mock_get):
        """测试获取单本书籍时出错"""
        # 配置模拟响应
        mock_get.side_effect = Exception("模拟的网络错误")
        
        # 调用客户端方法
        book, error = self.client.get_book(1)
        
        # 验证结果
        assert book is None
        assert error is not None
        assert "模拟的网络错误" in error
    
    @patch('client.book_client.requests.post')
    def test_create_book_success(self, mock_post):
        """测试成功创建书籍"""
        # 准备创建数据
        new_book_data = {
            "title": "新书籍",
            "author": "新作者",
            "publication_year": 2023,
            "isbn": "0123456789"
        }
        
        created_book = new_book_data.copy()
        created_book["id"] = 3
        
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": created_book}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # 调用客户端方法
        book, error = self.client.create_book(new_book_data)
        
        # 验证结果
        assert error is None
        assert book == created_book
        mock_post.assert_called_once_with(
            f"{self.base_url}/books",
            json=new_book_data,
            headers={'Content-Type': 'application/json'}
        )
    
    @patch('client.book_client.requests.post')
    def test_create_book_error(self, mock_post):
        """测试创建书籍时出错"""
        # 准备创建数据
        new_book_data = {
            "title": "新书籍",
            "author": "新作者"
        }
        
        # 配置模拟响应
        mock_post.side_effect = Exception("模拟的网络错误")
        
        # 调用客户端方法
        book, error = self.client.create_book(new_book_data)
        
        # 验证结果
        assert book is None
        assert error is not None
        assert "模拟的网络错误" in error
    
    @patch('client.book_client.requests.put')
    def test_update_book_success(self, mock_put):
        """测试成功更新书籍"""
        # 准备更新数据
        update_data = {
            "title": "更新的书籍",
            "author": "更新的作者"
        }
        
        updated_book = self.test_book.copy()
        updated_book.update(update_data)
        
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": updated_book}
        mock_response.raise_for_status.return_value = None
        mock_put.return_value = mock_response
        
        # 调用客户端方法
        book, error = self.client.update_book(1, update_data)
        
        # 验证结果
        assert error is None
        assert book == updated_book
        mock_put.assert_called_once_with(
            f"{self.base_url}/books/1",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
    
    @patch('client.book_client.requests.put')
    def test_update_book_error(self, mock_put):
        """测试更新书籍时出错"""
        # 准备更新数据
        update_data = {
            "title": "更新的书籍"
        }
        
        # 配置模拟响应
        mock_put.side_effect = Exception("模拟的网络错误")
        
        # 调用客户端方法
        book, error = self.client.update_book(1, update_data)
        
        # 验证结果
        assert book is None
        assert error is not None
        assert "模拟的网络错误" in error
    
    @patch('client.book_client.requests.delete')
    def test_delete_book_success(self, mock_delete):
        """测试成功删除书籍"""
        # 配置模拟响应
        mock_response = MagicMock()
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response
        
        # 调用客户端方法
        success, error = self.client.delete_book(1)
        
        # 验证结果
        assert error is None
        assert success is True
        mock_delete.assert_called_once_with(f"{self.base_url}/books/1")
    
    @patch('client.book_client.requests.delete')
    def test_delete_book_error(self, mock_delete):
        """测试删除书籍时出错"""
        # 配置模拟响应
        mock_delete.side_effect = Exception("模拟的网络错误")
        
        # 调用客户端方法
        success, error = self.client.delete_book(1)
        
        # 验证结果
        assert success is False
        assert error is not None
        assert "模拟的网络错误" in error 