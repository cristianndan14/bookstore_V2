from flask import request, jsonify
from flask_login import login_required, current_user

from ..models.SellsModel import SellsModel
from ..models.BookModel import BookModel

from ..models.entities.sells import Sells

from ..emails import order_mail_confirmation


def init_buyBook(app, db, mail):

    @app.route('/buyBook', methods=['POST'])
    @login_required
    def buy_book():
        data_request = request.get_json()
        data = {}
        try:
            book = BookModel.read_book(db, data_request['isbn'])
            order = Sells(None, book, current_user)
            data['Success'] = SellsModel.register_sell(db, order)
            # confirmacion_compra(mail, current_user, libro) # Envio normal.
            order_mail_confirmation(app, mail, current_user, book)  # Envio async.
        except Exception as ex:
            data['message'] = format(ex)
            data['success'] = False
        return jsonify(data)