import pytest
from server.models.book import Book
from server.models.database import Database
from server.controllers.book_controller import BookController

class TestBookController:
    """测试BookController类"""
    
    def setup_method(self):
        """每个测试方法运行前的设置"""
        self.db = Database()
        self.controller = BookController(self.db)
        
        # 添加一些测试数据
        self.test_book_data = {
            "title": "测试书籍",
            "author": "测试作者",
            "publication_year": 2022,
            "isbn": "1234567890"
        }
        self.controller.create_book(self.test_book_data)
    
    def test_get_all_books(self):
        """测试获取所有书籍"""
        # 添加多本书
        self.controller.create_book({
            "title": "书籍2",
            "author": "作者2",
            "publication_year": 2021,
            "isbn": "2222222222"
        })
        
        books = self.controller.get_all_books()
        
        assert len(books) == 2
        assert books[0]["title"] == "测试书籍"
        assert books[1]["title"] == "书籍2"
    
    def test_get_book(self):
        """测试获取单本书籍"""
        # 获取存在的书籍
        book, error = self.controller.get_book(1)
        
        assert error is None
        assert book is not None
        assert book["title"] == "测试书籍"
        assert book["author"] == "测试作者"
        
        # 获取不存在的书籍
        book, error = self.controller.get_book(999)
        
        assert book is None
        assert error is not None
        assert "找不到" in error
        
        # 使用无效ID
        book, error = self.controller.get_book("abc")
        
        assert book is None
        assert error is not None
        assert "无效" in error
    
    def test_create_book(self):
        """测试创建书籍"""
        new_book_data = {
            "title": "新书籍",
            "author": "新作者",
            "publication_year": 2023,
            "isbn": "9876543210"
        }
        
        book, error = self.controller.create_book(new_book_data)
        
        assert error is None
        assert book is not None
        assert book["id"] == 2  # 第二本书，ID应为2
        assert book["title"] == "新书籍"
        
        # 测试创建缺少字段的书籍
        incomplete_book_data = {
            "title": "不完整的书籍"
        }
        
        book, error = self.controller.create_book(incomplete_book_data)
        
        assert error is None  # 我们的实现允许缺少字段
        assert book is not None
        assert book["title"] == "不完整的书籍"
        assert book["author"] is None
    
    def test_update_book(self):
        """测试更新书籍"""
        update_data = {
            "title": "更新的书籍",
            "author": "更新的作者"
        }
        
        # 更新存在的书籍
        book, error = self.controller.update_book(1, update_data)
        
        assert error is None
        assert book is not None
        assert book["title"] == "更新的书籍"
        assert book["author"] == "更新的作者"
        # 其他字段应保持不变
        assert book["publication_year"] == 2022
        assert book["isbn"] == "1234567890"
        
        # 更新不存在的书籍
        book, error = self.controller.update_book(999, update_data)
        
        assert book is None
        assert error is not None
        assert "找不到" in error
        
        # 使用无效ID
        book, error = self.controller.update_book("abc", update_data)
        
        assert book is None
        assert error is not None
        assert "无效" in error
    
    def test_delete_book(self):
        """测试删除书籍"""
        # 删除存在的书籍
        success, error = self.controller.delete_book(1)
        
        assert error is None
        assert success is True
        
        # 验证书籍已被删除
        book, _ = self.controller.get_book(1)
        assert book is None
        
        # 删除不存在的书籍
        success, error = self.controller.delete_book(999)
        
        assert success is False
        assert error is not None
        assert "找不到" in error
        
        # 使用无效ID
        success, error = self.controller.delete_book("abc")
        
        assert success is False
        assert error is not None
        assert "无效" in error 