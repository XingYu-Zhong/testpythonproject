import pytest
from server.models.book import Book
from server.models.database import Database

class TestBook:
    """测试Book模型类"""
    
    def test_book_creation(self):
        """测试创建Book对象"""
        book = Book(1, "Python编程", "张三", 2020, "9787111612727")
        
        assert book.book_id == 1
        assert book.title == "Python编程"
        assert book.author == "张三"
        assert book.publication_year == 2020
        assert book.isbn == "9787111612727"
    
    def test_book_to_dict(self):
        """测试Book对象转换为字典"""
        book = Book(1, "Python编程", "张三", 2020, "9787111612727")
        book_dict = book.to_dict()
        
        assert book_dict["id"] == 1
        assert book_dict["title"] == "Python编程"
        assert book_dict["author"] == "张三"
        assert book_dict["publication_year"] == 2020
        assert book_dict["isbn"] == "9787111612727"
    
    def test_book_from_dict(self):
        """测试从字典创建Book对象"""
        book_dict = {
            "id": 1,
            "title": "Python编程",
            "author": "张三",
            "publication_year": 2020,
            "isbn": "9787111612727"
        }
        
        book = Book.from_dict(book_dict)
        
        assert book.book_id == 1
        assert book.title == "Python编程"
        assert book.author == "张三"
        assert book.publication_year == 2020
        assert book.isbn == "9787111612727"
    
    def test_book_from_dict_missing_fields(self):
        """测试从不完整的字典创建Book对象"""
        book_dict = {
            "title": "Python编程",
            "author": "张三"
        }
        
        book = Book.from_dict(book_dict)
        
        assert book.book_id is None
        assert book.title == "Python编程"
        assert book.author == "张三"
        assert book.publication_year is None
        assert book.isbn is None


class TestDatabase:
    """测试Database类"""
    
    def setup_method(self):
        """每个测试方法运行前的设置"""
        self.db = Database()
        self.test_book = Book(None, "测试书籍", "测试作者", 2022, "1234567890")
    
    def test_add_book(self):
        """测试添加书籍"""
        book = self.db.add_book(self.test_book)
        
        assert book.book_id == 1  # 自动分配ID=1
        assert len(self.db.books) == 1
        assert self.db.books[1] == book
    
    def test_get_book_by_id(self):
        """测试通过ID获取书籍"""
        self.db.add_book(self.test_book)
        book = self.db.get_book_by_id(1)
        
        assert book is not None
        assert book.title == "测试书籍"
        
        # 测试获取不存在的书籍
        non_existent_book = self.db.get_book_by_id(999)
        assert non_existent_book is None
    
    def test_get_all_books(self):
        """测试获取所有书籍"""
        # 先添加多本书
        self.db.add_book(Book(None, "书籍1", "作者1", 2020, "1111111111"))
        self.db.add_book(Book(None, "书籍2", "作者2", 2021, "2222222222"))
        self.db.add_book(Book(None, "书籍3", "作者3", 2022, "3333333333"))
        
        books = self.db.get_all_books()
        
        assert len(books) == 3
        assert books[0].title == "书籍1"
        assert books[1].title == "书籍2"
        assert books[2].title == "书籍3"
    
    def test_update_book(self):
        """测试更新书籍"""
        self.db.add_book(self.test_book)
        
        updated_book = Book(1, "更新的书籍", "更新的作者", 2023, "9876543210")
        success = self.db.update_book(1, updated_book)
        
        assert success is True
        book = self.db.get_book_by_id(1)
        assert book.title == "更新的书籍"
        assert book.author == "更新的作者"
        
        # 测试更新不存在的书籍
        non_existent_update = self.db.update_book(999, updated_book)
        assert non_existent_update is False
    
    def test_delete_book(self):
        """测试删除书籍"""
        self.db.add_book(self.test_book)
        
        # 确认书籍存在
        assert len(self.db.get_all_books()) == 1
        
        # 删除书籍
        success = self.db.delete_book(1)
        assert success is True
        assert len(self.db.get_all_books()) == 0
        
        # 测试删除不存在的书籍
        non_existent_delete = self.db.delete_book(999)
        assert non_existent_delete is False 