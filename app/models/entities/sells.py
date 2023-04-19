import datetime


class Sells:

    def __init__(self, uuid, isbn_book, id_user, datetime=None):
        self.uuid = uuid
        self.isbn_book = isbn_book
        self.id_user = id_user
        self.datetime = datetime

    def formatted_date(self):
        return datetime.datetime.strftime(self.datetime, '%d/%m/%Y - %H:%M:%S')
