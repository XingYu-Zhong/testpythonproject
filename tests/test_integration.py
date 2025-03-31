import pytest
import threading
import time
import requests

from server.models import Book, Database
from server.controllers import BookController
from server.views import BookView
from server.server import BookServer
from client.book_client import BookClient

@pytest.fixture
def server():
    """启动测试服务器的fixture"""
    # 使用一个不太可能冲突的端口
    port = 8099
    server = BookServer(port=port)
    
    # 启动服务器
    server.start()
    
    # 确保服务器已启动
    time.sleep(1)
    
    yield server
    
    # 测试完成后关闭服务器
    server.stop()

@pytest.fixture
def client(server):
    """创建一个客户端实例，连接到测试服务器"""
    return BookClient(f"http://localhost:{server.port}")

class TestIntegration:
    """集成测试，测试服务器和客户端的交互"""
    
    def test_server_is_running(self, server):
        """测试服务器是否正在运行"""
        try:
            response = requests.get(f"http://localhost:{server.port}/books")
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.fail("无法连接到服务器")
    
    def test_get_all_books(self, client):
        """测试获取所有书籍"""
        books, error = client.get_all_books()
        
        assert error is None
        assert books is not None
        # 服务器启动时会添加一些示例数据
        assert len(books) >= 3
    
    def test_crud_operations(self, client):
        """测试完整的CRUD操作流程"""
        # 1. 创建书籍
        new_book_data = {
            "title": "集成测试书籍",
            "author": "测试作者",
            "publication_year": 2023,
            "isbn": "1122334455"
        }
        
        created_book, error = client.create_book(new_book_data)
        assert error is None
        assert created_book is not None
        assert created_book["title"] == "集成测试书籍"
        
        book_id = created_book["id"]
        
        # 2. 获取创建的书籍
        book, error = client.get_book(book_id)
        assert error is None
        assert book is not None
        assert book["title"] == "集成测试书籍"
        
        # 3. 更新书籍
        update_data = {
            "title": "更新的集成测试书籍",
            "author": "更新的测试作者"
        }
        
        updated_book, error = client.update_book(book_id, update_data)
        assert error is None
        assert updated_book is not None
        assert updated_book["title"] == "更新的集成测试书籍"
        assert updated_book["author"] == "更新的测试作者"
        # 确保其他字段保持不变
        assert updated_book["publication_year"] == 2023
        
        # 4. 获取更新后的书籍
        book, error = client.get_book(book_id)
        assert error is None
        assert book["title"] == "更新的集成测试书籍"
        
        # 5. 删除书籍
        success, error = client.delete_book(book_id)
        assert error is None
        assert success is True
        
        # 6. 确保书籍已被删除
        book, error = client.get_book(book_id)
        assert book is None
        assert error is not None
    
    def test_get_nonexistent_book(self, client):
        """测试获取不存在的书籍"""
        book, error = client.get_book(9999)
        
        assert book is None
        assert error is not None
        assert "找不到" in error or "404" in error
    
    def test_delete_nonexistent_book(self, client):
        """测试删除不存在的书籍"""
        success, error = client.delete_book(9999)
        
        assert success is False
        assert error is not None 