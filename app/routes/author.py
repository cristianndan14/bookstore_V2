from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from ..models.AuthorModel import AuthorModel

from ..models.entities.author import Author


def init_author(app, db):

    @app.route('/authors')
    @login_required
    def author_list():
        try:
            authors = AuthorModel.author_list(db)
            data = {
                'title': 'Author list',
                'authors': authors
            }
            return render_template('author_list.html', data=data)
        except Exception as ex:
            return render_template('errors/error.html', message=format(ex))

    @app.route('/authors/add_author', methods=['GET', 'POST'])
    @login_required
    def add_author():
        if current_user.user_type_id.id == 1:
            try:
                if request.method == 'POST':
                    last_name = request.form['last_name']
                    name = request.form['name']
                    birth_date = request.form['birth_date']

                    new_author = Author(None, last_name,
                                        name, birth_date)

                    add_author = AuthorModel.add_author(db, new_author)

                    if add_author != None:
                        """AGREGAR flashmessages"""
                        return redirect(url_for('authors'))
                    else:
                        return render_template('add_author.html')

                return render_template('add_author.html')

            except Exception as ex:
                return render_template('errors/error.html', message=format(ex))
        else:
            return redirect(url_for('authors'))
