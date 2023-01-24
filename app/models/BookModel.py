from .entities.author import Author
from .entities.book import Book


class BookModel():

    @classmethod
    def book_list(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT B.isbn, B.title, B.publication_date, B.price, 
                AUT.last_name, AUT.name
                FROM book B JOIN author AUT ON B.id_author = AUT.id_author
                ORDER BY B.title ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            books = []
            for row in data:
                aut = Author(0, row[4], row[5])
                b = Book(row[0], row[1], aut, row[2], row[3])
                books.append(b)
            return books
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def read_book(cls, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, title, publication_date, price
                    FROM book WHERE isbn = '{0}'""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()
            book = Book(data[0], data[1], None, data[2], data[3])
            return book
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def book_lists_sold(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT S.isbn_book, B.title, B.price,
                        COUNT(S.isbn_book) AS items_sold
                        FROM sells S JOIN book B ON S.isbn_book = B.isbn
                        GROUP BY S.isbn_book
                        ORDER BY 4 DESC, 2 ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            books = []
            for row in data:
                b = Book(row[0], row[1], None, None, row[2])
                b.items_sold = int(row[3])
                books.append(b)
            return books
        except Exception as ex:
            raise Exception(ex)
