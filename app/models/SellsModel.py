from .entities.sells import Sells
from .entities.book import Book


class SellsModel():

    @classmethod
    def register_sell(cls, db, sell):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO sells (uuid, isbn_book, id_user)
                        VALUES (uuid(), '{0}', {1})""".format(sell.isbn_book.isbn, sell.id_user.id)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def list_user_purchases(cls, db, user):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT S.datetime, B.isbn, B.title, B.price, B.cover
                    FROM sells S JOIN book B ON S.isbn_book = B.isbn
                    WHERE S.id_user = {0}""".format(user.id_user)
            cursor.execute(sql)
            data = cursor.fetchall()
            sells = []
            for row in data:
                b = Book(row[1], row[2], None, None, row[3], row[4])
                s = Sells(None, b, user, row[0])
                sells.append(s)
            return sells
        except Exception as ex:
            raise Exception(ex)
