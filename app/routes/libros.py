from flask import render_template
from flask_login import login_required

from ..models.ModeloLibro import ModeloLibro


def init_libros(app, db):

    @app.route('/libros')
    @login_required
    def listar_libros():
        try:
            libros = ModeloLibro.listar_libro(db)
            data = {
                'titulo': 'Listado de libros',
                'libros': libros
            }
            return render_template('listado_libros.html', data=data)
        except Exception as ex:
            return render_template('errores/error.html', mensaje=format(ex))