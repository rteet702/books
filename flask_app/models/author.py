from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import book


class Author:
    def __init__(self, data:dict) -> None:
        self.id = data.get('id')
        self.name = data.get('name')
        self.created_at = data.get('created_at')
        self.updated_at = data.get('updated_at')
        self.favorites = []

    @classmethod
    def get_all_authors(cls) -> list:
        query = "SELECT * FROM authors;"
        results = connectToMySQL('books').query_db(query)
        authors = []

        for row in results:
            authors.append(cls(row))

        return authors

    @classmethod
    def add_author(cls, data:dict) -> int:
        query = "INSERT INTO authors (name) VALUES (%(name)s);"

        return connectToMySQL('books').query_db(query, data)

    @classmethod
    def get_author_by_id(cls, data:dict) -> object:
        query = "SELECT * FROM authors WHERE id = %(id)s;"
        result = connectToMySQL('books').query_db(query, data)

        return cls(result[0])

    @classmethod
    def add_favorite(cls, data:dict) -> int:
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s, %(book_id)s);"

        return connectToMySQL('books').query_db(query, data)

    @classmethod
    def get_author_with_favorites(cls, data:dict) -> object:
        query = """SELECT books.title, books.num_of_pages, books.created_at, books.updated_at FROM favorites
                    JOIN authors ON author_id = authors.id
                    JOIN books ON book_id = books.id
                    WHERE authors.id = %(id)s;"""

        results = connectToMySQL('books').query_db(query, data)
        author = cls.get_author_by_id(data)

        for row in results:
            author.favorites.append(book.Book(row))

        return author