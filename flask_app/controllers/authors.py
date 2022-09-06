from flask_app.models.author import Author
from flask_app.models.book import Book
from flask_app import app
from flask import render_template, redirect, request


@app.route('/authors')
def r_authors():
    all_authors = Author.get_all_authors()
    return render_template('authors.html', all_authors=all_authors)


@app.route('/authors/submit', methods=['POST'])
def f_authors_submit():
    data = {
        'name': request.form.get('name')
    }
    Author.add_author(data)

    return redirect('/authors')


@app.route('/authors/<int:id>')
def r_view_author(id):
    data = {'id': id}
    author = Author.get_author_with_favorites(data)
    all_books = Book.get_all_books()

    return render_template('view_author.html', author=author, all_books=all_books)


@app.route('/authors/<int:id>/add', methods=['POST'])
def f_add_favorite_to_author(id):
    data = {
        'author_id': id,
        'book_id': request.form.get('book')
    }
    Author.add_favorite(data)

    return redirect(f'/authors/{id}')