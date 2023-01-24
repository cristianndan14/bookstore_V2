from flask import render_template, request
from flask_login import login_required, current_user
from isbnlib import isbn_from_words

from ..models.BookModel import BookModel
from ..models.AuthorModel import AuthorModel


def init_book(app, db):

    @app.route('/books')
    @login_required
    def book_list():
        try:
            books = BookModel.book_list(db)
            data = {
                'title': 'Book list',
                'books': books
            }
            return render_template('book_list.html', data=data)
        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))

    @app.route('/books/add_book', methods=['GET', 'POST'])
    @login_required
    def add_book():
        try:
            authors = AuthorModel.author_list(db)
            data = {
                'authors': authors
            }
            if request.method == 'POST':
                isbn = isbn_from_words(request.form['Title'])
                title = request.form['Title']
                author = request.form['Author']
                publication_date = request.form['publication_date']
                price = request.form['Price']

            return render_template('add_book.html', data=data)
        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))