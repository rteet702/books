from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author


class Book:
    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.title = data.get('title')
        self.num_of_pages = data.get('num_of_pages')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.favorited_by = []

    @classmethod
    def get_all_books(cls) -> list:
        query = "SELECT * FROM books"
        results = connectToMySQL('books').query_db(query)
        books = []

        for row in results:
            books.append(cls(row))

        return books

    @classmethod
    def add_book(cls, data:dict) -> int:
        query = "INSERT INTO books (title, num_of_pages) VALUES (%(title)s, %(num_of_pages)s);"

        return connectToMySQL('books').query_db(query, data)

    @classmethod
    def get_book_by_id(cls, data:dict) -> object:
        query = "SELECT * FROM books WHERE id = %(id)s;"
        result = connectToMySQL('books').query_db(query, data)

        return cls(result[0])

    @classmethod
    def get_book_with_favorites(cls, data:dict) -> object:
        query = """SELECT authors.name, authors.created_at, authors.updated_at FROM favorites
                    JOIN authors ON author_id = authors.id
                    JOIN books ON book_id = books.id
                    WHERE books.id = %(id)s;"""

        results = connectToMySQL('books').query_db(query, data)
        book = cls.get_book_by_id(data)

        for row in results:
            book.favorited_by.append(author.Author(row))

        return book