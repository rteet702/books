from flask_app.models.book import Book
from flask_app.models.author import Author
from flask_app import app
from flask import render_template, redirect, request


@app.route('/books')
def r_books():
    all_books = Book.get_all_books()
    return render_template('books.html', all_books=all_books)

@app.route('/books/submit', methods=['POST'])
def f_books_submit():
    data = {
        'title': request.form.get('title'),
        'num_of_pages': request.form.get('num_of_pages')
    }
    Book.add_book(data)
    return redirect('/books')


@app.route('/books/<int:id>')
def r_view_book(id):
    data = {'id': id}
    book = Book.get_book_with_favorites(data)
    all_authors = Author.get_all_authors()
    return render_template('view_book.html', book=book, all_authors=all_authors)


@app.route('/books/<int:id>/add', methods=['POST'])
def f_add_favorite_to_book(id):
    data = {
        'author_id': request.form.get('author'),
        'book_id': id
    }
    Author.add_favorite(data)

    return redirect(f'/books/{id}')