class Book:
    def __init__(self, book_id, title, author, publication_year, isbn):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.publication_year = publication_year
        self.isbn = isbn
    
    def to_dict(self):
        return {
            "id": self.book_id,
            "title": self.title,
            "author": self.author,
            "publication_year": self.publication_year,
            "isbn": self.isbn
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            book_id=data.get("id"),
            title=data.get("title"),
            author=data.get("author"),
            publication_year=data.get("publication_year"),
            isbn=data.get("isbn")
        ) 