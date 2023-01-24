from flask import Flask
from flask_login import LoginManager
from flask_mysqldb import MySQL
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail

from .models.UserModel import UserModel

from .routes.auth import init_auth
from .routes.buyBook import init_buyBook
from .routes.index import init_index
from .routes.books import init_book
from .routes.errors import init_errors

app = Flask(__name__)

csrf = CSRFProtect()

db = MySQL(app)
login_manager_app = LoginManager(app)
mail = Mail(app)


init_auth(app, db)
init_buyBook(app, db, mail)
init_index(app, db)
init_book(app, db)
init_errors(app)


@login_manager_app.user_loader
def load_user(id):
    return UserModel.get_user_id(db, id)


def run_app(config):
    app.config.from_object(config)
    csrf.init_app(app)
    mail.init_app(app)
    return app
