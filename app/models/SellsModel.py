from .entities.sells import Sells
from .entities.book import Book


class SellsModel():

    @classmethod
    def register_sell(cls, db, sell):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO sells (uuid, isbn_book, id_user)
                        VALUES (uuid(), '{0}', {1})""".format(sell.book.isbn, sell.users.id)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def list_user_purchases(cls, db, users):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT S.datetime, B.isbn, B.title, B.price 
                    FROM sells S JOIN book B ON S.isbn_book = B.isbn
                    WHERE S.id_user = {0}""".format(users.id)
            cursor.execute(sql)
            data = cursor.fetchall()
            sells = []
            for row in data:
                b = Book(row[1], row[2], None, None, row[3])
                s = Sells(None, b, users, row[0])
                sells.append(s)
            return sells
        except Exception as ex:
            raise Exception(ex)
