from decouple import config


class Config:
    SECRET_KEY = 'bM#@zeMW85axLe8Tsh'
    UPLOAD_COVERS = 'app/static/img/covers'
    UPLOAD_AUTHORS = 'app/static/img/authors'
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = '127.0.0.1'
    MYSQL_PORT = 3306
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = config('MYSQL_PASSWORD')
    MYSQL_DB = 'bookstore'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587  # TLS Transpor Layer Security
    MAIL_USE_TLS = True
    MAIL_USERNAME = config('MAIL_USERNAME')
    MAIL_PASSWORD = config('MAIL_PASSWORD')


config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}
