from werkzeug.security import check_password_hash
from flask_login import UserMixin


class Usuario(UserMixin):

    def __init__(self, id, usuario, password, tipousuario_id):
        self.id = id
        self.usuario = usuario
        self.password = password
        self.tipousuario_id = tipousuario_id

    @classmethod
    def verificar_password(cls, encriptado, password):
        return check_password_hash(encriptado, password)
