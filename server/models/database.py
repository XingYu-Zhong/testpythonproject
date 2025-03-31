class Database:
    def __init__(self):
        self.books = {}
        self.next_id = 1
    
    def get_all_books(self):
        return list(self.books.values())
    
    def get_book_by_id(self, book_id):
        return self.books.get(book_id)
    
    def add_book(self, book):
        if book.book_id is None:
            book.book_id = self.next_id
            self.next_id += 1
        self.books[book.book_id] = book
        return book
    
    def update_book(self, book_id, updated_book):
        if book_id in self.books:
            updated_book.book_id = book_id
            self.books[book_id] = updated_book
            return True
        return False
    
    def delete_book(self, book_id):
        if book_id in self.books:
            del self.books[book_id]
            return True
        return False 