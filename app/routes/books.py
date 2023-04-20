import os
from flask import current_app
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from isbnlib import isbn_from_words
from werkzeug.utils import secure_filename

from ..models.BookModel import BookModel
from ..models.AuthorModel import AuthorModel

from ..models.entities.book import Book
from ..models.entities.author import Author

from ..consts import *


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']



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
                if request.method == 'POST':
                    isbn = isbn_from_words(request.form['Title'])
                    title = request.form['Title']
                    author_name = request.form['Author_name']
                    author_lastname = request.form['Author_lastname']
                    author_birthdate = request.form['Author_birthdate']
                    publication_date = request.form['Publication_date']
                    price = request.form['Price']

                    # Check if file was uploaded
                    if 'customFile' not in request.files:
                        flash('No file part')
                        return redirect(request.url)
                    file = request.files['customFile']
                    if file.filename == '':
                        flash('No selected file')
                        return redirect(request.url)
                    if not allowed_file(file.filename):
                        flash('Invalid file type')
                        return redirect(request.url)
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    cover_route = f'/img/covers/{filename}'


                    new_author = Author(None, author_name, author_lastname, author_birthdate)

                    add_author = AuthorModel.add_author(db, new_author)

                    if add_author != None:
                        id_author = len(authors) + 1
                        new_book = Book(isbn, title, id_author,
                                        publication_date, price, cover_route)
                        add_book = BookModel.add_book(db, new_book)

                        if add_book != None:
                            flash(ADD_BOOK_SUCCESS, 'success')
                            return redirect(url_for('book_list'))
                        else:
                            return render_template('add_book.html')
                    else:
                            return render_template('add_book.html')

                return render_template('add_book.html')

            except Exception as ex:
                print(ex)
                return render_template('errors/error.html', message=format(ex))
        else:
            return redirect(url_for('books'))
