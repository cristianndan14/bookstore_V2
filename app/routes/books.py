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
                authors_dict = AuthorModel.author_list(db)
                # IMPLEMENTAR FOR DENTRO DEL IF
                """ for author_id, author_info in authors_dict.items():
                    if author_info['name'] == 'Ryan' and author_info['last_name'] == 'Holyday':
                        print(f"ID del autor: {author_id}")
                        print(f"Nombre completo: {author_info['name']} {author_info['last_name']}")
                        print(f"Fecha de nacimiento: {author_info['birth_date']}")
                        break
                    else:
                        print("No se encontró ningún autor con ese nombre.") """
                if request.method == 'POST':
                    isbn = isbn_from_words(request.form['Title'])
                    title = request.form['Title']
                    author_name = request.form['Author_name']
                    author_lastname = request.form['Author_lastname']
                    author_birthdate = request.form['Author_birthdate']
                    publication_date = request.form['Publication_date']
                    price = request.form['Price']
                    file = request.files['customFile']
                    
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    cover_route = f'/img/covers/{filename}'

                    new_author = Author(None, author_name, author_lastname, author_birthdate)
                    add_author = AuthorModel.add_author(db, new_author)


                    if add_author != None and add_book != None:
                        id_author = len(authors_dict) + 1
                        new_book = Book(isbn, title, id_author, publication_date, price, cover_route)
                        add_book = BookModel.add_book(db, new_book)

                        flash(ADD_BOOK_SUCCESS, 'success')
                        return redirect(url_for('book_list'))
                    else:
                        return render_template('add_book.html')

                return render_template('add_book.html')

            except Exception as ex:
                print(ex)
                return render_template('errors/error.html', message=format(ex))
        else:
            return redirect(url_for('books'))
