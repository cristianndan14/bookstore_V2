from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

from .models.ModeloUsuario import ModeloUsuario

from .routes.auth import init_auth
from .routes.comprarLibro import init_comprarLibro
from .routes.index import init_index
from .routes.libros import init_libros
from .routes.errores import init_errors

app = Flask(__name__)

csrf = CSRFProtect()

db = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail(app)


init_auth(app, db)
init_comprarLibro(app, db, mail)
init_index(app, db)
init_libros(app, db)
init_errors(app)


@login_manager_app.user_loader
def load_user(id):
    return ModeloUsuario.obtener_por_id(db, id)


def inicializar_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    mail.init_app(app)
    return app
