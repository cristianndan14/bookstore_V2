import datetime


class Sells:

    def __init__(self, uuid, book_isbn, user_id, datetime=None):
        self.uuid = uuid
        self.book_isbn = book_isbn
        self.user_id = user_id
        self.datetime = datetime

    def formatted_date(self):
        return datetime.datetime.strftime(self.datetime, '%d/%m/%Y - %H:%M:%S')
