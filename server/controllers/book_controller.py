import json
from server.models.book import Book

class BookController:
    def __init__(self, database):
        self.database = database
    
    def get_all_books(self):
        books = self.database.get_all_books()
        return [book.to_dict() for book in books]
    
    def get_book(self, book_id):
        try:
            book_id = int(book_id)
        except ValueError:
            return None, "无效的书籍ID"
        
        book = self.database.get_book_by_id(book_id)
        if book:
            return book.to_dict(), None
        return None, "找不到指定的书籍"
    
    def create_book(self, book_data):
        try:
            book = Book.from_dict(book_data)
            book = self.database.add_book(book)
            return book.to_dict(), None
        except Exception as e:
            return None, f"创建书籍失败: {str(e)}"
    
    def update_book(self, book_id, book_data):
        try:
            book_id = int(book_id)
        except ValueError:
            return None, "无效的书籍ID"
        
        book = Book.from_dict(book_data)
        success = self.database.update_book(book_id, book)
        if success:
            return book.to_dict(), None
        return None, "找不到指定的书籍"
    
    def delete_book(self, book_id):
        try:
            book_id = int(book_id)
        except ValueError:
            return False, "无效的书籍ID"
        
        success = self.database.delete_book(book_id)
        if success:
            return True, None
        return False, "找不到指定的书籍" 