from .entities.author import Author

class AuthorModel():

    @classmethod
    def author_list(cls, db):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT name, last_name FROM author"""
            cursor.execute(sql)
            data = cursor.fetchall()
            authors = []
            for row in data:
                aut = Author(0, row[0], row[1])
                authors.append(aut)
            return authors
        except Exception as ex:
            raise Exception(ex)