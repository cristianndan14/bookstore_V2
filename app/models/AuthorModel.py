from .entities.author import Author

import pymysql


class AuthorModel():

    @classmethod
    def author_list(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_author, name, last_name, birth_date FROM author"""
            cursor.execute(sql)
            data = cursor.fetchall()
            authors = [Author(*row) for row in data]
            return authors
        except Exception as ex:
            raise Exception(ex)
        finally:
            cursor.close()

    @classmethod
    def add_author(cls, db, author):
        """ if author.last_name or not author.name or not author.birth_date:
            raise ValueError("All fields are required!")"""
            
        error_msg = None

        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO author(id_author, last_name, name, birth_date)
                            VALUES(0, %s, %s, %s)"""
            cursor.execute(
                sql,
                (author.last_name, author.name,
                 author.birth_date,)
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
