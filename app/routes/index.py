from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from ..models.SellsModel import SellsModel
from ..models.BookModel import BookModel


def init_index(app, db):

    @app.route('/')
    @login_required
    def index():
        if current_user.is_authenticated:
            if current_user.user_type_id.id == 1:
                try:
                    books_sold = BookModel.book_lists_sold(db)
                    data = {
                        'title': 'Books sold',
                        'books_sold': books_sold
                    }
                    return render_template('index.html', data=data)
                except Exception as ex:
                    return render_template('errors/error.html', message=format(ex))
            else:
                try:
                    orders = SellsModel.list_user_purchases(db, current_user)
                    data = {
                        'title': 'My purchases',
                        'orders': orders
                    }
                    return render_template('index.html', data=data)
                except Exception as ex:
                    return render_template('errors/error.html', message=format(ex))
        else:
            return redirect(url_for('login'))
