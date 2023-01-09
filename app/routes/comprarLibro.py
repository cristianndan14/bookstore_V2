from flask import request, jsonify
from flask_login import login_required, current_user

from ..models.ModeloCompra import ModeloCompra
from ..models.ModeloLibro import ModeloLibro

from ..models.entities.Compra import Compra

from ..emails import confirmacion_compra


def init_comprarLibro(app, db, mail):

    @app.route('/comprarLibro', methods=['POST'])
    @login_required
    def comprar_libro():
        data_request = request.get_json()
        data = {}
        try:
            libro = ModeloLibro.leer_libro(db, data_request['isbn'])
            compra = Compra(None, libro, current_user)
            data['exito'] = ModeloCompra.registrar_compra(db, compra)
            # confirmacion_compra(mail, current_user, libro) # Envio normal.
            confirmacion_compra(app, mail, current_user, libro)  # Envio async.
        except Exception as ex:
            data['mensaje'] = format(ex)
            data['exito'] = False
        return jsonify(data)