from werkzeug.security import check_password_hash
from flask_login import UserMixin


class User(UserMixin):

    def __init__(self, id_user, username, password, user_type_id, email, name, last_name):
        self.id_user = id_user
        self.username = username
        self.password = password
        self.user_type_id = user_type_id
        self.email = email
        self.name = name
        self.last_name = last_name

    @classmethod
    def verify_password(cls, encrypted, password):
        return check_password_hash(encrypted, password)
