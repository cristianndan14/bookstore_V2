from .entities.users import User
from .entities.user_type import UserType
import pymysql


class UserModel():

    @classmethod
    def login(cls, db, user):
        logged_user = None

        try:
            cursor = db.connection.cursor()
            sql = """SELECT id_user, username, password 
                    FROM user WHERE username = %s"""
            cursor.execute(sql, (user.username,))
            data = cursor.fetchone()
            if data:
                match = User.verify_password(data[2], user.password)
                if match:
                    logged_user = User(
                        data[0], data[1], None, None, None, None, None
                    )
                else:
                    return False
            else:
                return False
        except pymysql.Error as ex:
            return False
        finally:
            cursor.close()
        return logged_user

    @classmethod
    def get_user_id(cls, db, id):
        logged_user = None

        try:
            cursor = db.connection.cursor()
            sql = """SELECT U.id_user, U.username, UT.id_user_type, UT.type 
                    FROM user U JOIN user_type UT ON U.id_user_type = UT.id_user_type
                    WHERE U.id_user = %s"""
            cursor.execute(sql, (id,))
            data = cursor.fetchone()
            if data:
                user_type = UserType(data[2], data[3])
                logged_user = User(
                    data[0], data[1], None, user_type, None, None, None
                )
            else:
                return False
        except pymysql.Error as ex:
            return False
        finally:
            cursor.close()
        return logged_user

    @classmethod
    def create_user(cls, db, user):
        error_msg = None

        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO user (id_user, username, password, id_user_type, email, name, last_name)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql,
                           (user.id, user.username, user.password,
                            user.user_type_id, user.email, user.name, user.last_name,)
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

    @classmethod
    def verify_user(cls, db, username):
        result = None

        try:
            cursor = db.connection.cursor()
            sql = """SELECT 1
                FROM user
                WHERE username = %s"""
            cursor.execute(sql, (username,))
            result = cursor.fetchone() is not None
        except pymysql.Error as ex:
            raise ValueError(ex)
        finally:
            cursor.close()
        return result
