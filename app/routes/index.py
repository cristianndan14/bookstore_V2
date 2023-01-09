from flask import render_template, redirect, url_for
from flask_login import login_required, current_user

from ..models.ModeloCompra import ModeloCompra
from ..models.ModeloLibro import ModeloLibro


def init_index(app, db):

    @app.route('/')
    @login_required
    def index():
        if current_user.is_authenticated:
            if current_user.tipousuario_id.id == 1:
                try:
                    libros_vendidos = ModeloLibro.listar_libros_vendidos(db)
                    data = {
                        'titulo': 'Libros vendidos',
                        'libros_vendidos': libros_vendidos
                    }
                    return render_template('index.html', data=data)
                except Exception as ex:
                    return render_template('errores/error.html', mensaje=format(ex))
            else:
                try:
                    compras = ModeloCompra.listar_compras_usuario(db, current_user)
                    data = {
                        'titulo': 'Mis compras',
                        'compras': compras
                    }
                    return render_template('index.html', data=data)
                except Exception as ex:
                    return render_template('errores/error.html', mensaje=format(ex))
        else:
            return redirect(url_for('login'))
