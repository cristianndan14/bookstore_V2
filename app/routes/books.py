from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user
from isbnlib import isbn_from_words

from ..models.BookModel import BookModel
from ..models.AuthorModel import AuthorModel

from ..models.entities.book import Book


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
        if current_user.user_type_id.id == 1:
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
                    cover = request.files.get('cover')

                    cover.save(f'static/img/covers/{cover.filename}')
                    cover_route = f'static/img/covers/{cover.filename}'

                    new_book = Book(isbn, title, author,
                                    publication_date, price, cover_route)

                    add_book = BookModel.add_book(db, new_book)

                    if add_book != None:
                        """AGREGAR flashmessages"""
                        return redirect(url_for('books'))
                    else:
                        return render_template('add_book.html', data=data)

                return render_template('add_book.html', data=data)

            except Exception as ex:
                return render_template('errors/error.html', message=format(ex))
        else:
            return redirect(url_for('books'))
