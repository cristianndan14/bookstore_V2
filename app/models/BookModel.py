from .entities.author import Author
from .entities.book import Book

import pymysql


class BookModel():

    @classmethod
    def book_list(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT B.isbn, B.title, B.publication_date, B.price, B.cover, 
                AUT.last_name, AUT.name
                FROM book B JOIN author AUT ON B.id_author = AUT.id_author
                ORDER BY B.title ASC"""
            cursor.execute(sql)
            data = cursor.fetchall()
            books = []
            for row in data:
                aut = Author(0, row[5], row[6])
                b = Book(row[0], row[1], aut, row[2], row[3], row[4])
                books.append(b)
            return books
        except Exception as ex:
            raise Exception(ex)

        finally:
            cursor.close()

    @classmethod
    def read_book(cls, db, isbn):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT isbn, title, publication_date, price, cover
                    FROM book WHERE isbn = '{0}'""".format(isbn)
            cursor.execute(sql)
            data = cursor.fetchone()
            book = Book(data[0], data[1], None, data[2], data[3], data[4])
            return book
        except Exception as ex:
            raise Exception(ex)

        finally:
            cursor.close()

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
                b = Book(row[0], row[1], None, None, row[2], None)
                b.items_sold = int(row[3])
                books.append(b)
            return books
        except Exception as ex:
            raise Exception(ex)

        finally:
            cursor.close()

    @classmethod
    def add_book(cls, db, book):
        """ if not book.isbn or not book.title or not book.author or not book.publication_date or not book.price or not book.cover:
            raise ValueError("All fields are required!") """

        error_msg = None

        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO book(isbn, title, id_author, publication_date, price, cover)
                            VALUES(%s, %s, %s, %s, %s, %s)"""
            cursor.execute(
                sql,
                (book.isbn, book.title, book.id_author,
                 book.publication_date, book.price, book.cover,)
            )
            db.connection.commit()

        except pymysql.Error as ex:
            error_msg = ex.args[1]
            db.connection.rollback()

        finally:
            cursor.close()

        if error_msg:
            raise ValueError(error_msg)
        return True
