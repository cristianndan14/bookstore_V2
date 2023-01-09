from .entities.Usuario import Usuario
from .entities.TipoUsuario import TipoUsuario


class ModeloUsuario():

    @classmethod
    def login(cls, db, usuario):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT id, usuario, password 
                    FROM usuario WHERE usuario = '{0}'""".format(usuario.usuario)
            cursor.execute(sql)
            data = cursor.fetchone()
            if data != None:
                coincide = Usuario.verificar_password(
                    data[2], usuario.password)
                if coincide:
                    usuario_logueado = Usuario(data[0], data[1], None, None)
                    return usuario_logueado
                else:
                    return None
            else:
                return None
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def obtener_por_id(cls, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT USU.id, USU.usuario, USU.password, TIP.id, TIP.nombre 
                    FROM usuario USU JOIN tipousuario TIP ON USU.tipousuario_id = TIP.id
                    WHERE USU.id = {0}""".format(id)
            cursor.execute(sql)
            data = cursor.fetchone()
            tipousuario = TipoUsuario(data[3], data[4])
            usuario_logueado = Usuario(data[0], data[1], None, tipousuario)
            return usuario_logueado
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def crear_nuevo_usuario(cls, db, usuario):
        try:
            cursor = db.connection.cursor()
            sql = """INSERT INTO usuario (id, usuario, password, tipousuario_id)
                        VALUES ('{0}', '{1}', '{2}', '{3}')""".format(usuario.id, usuario.usuario, usuario.password, usuario.tipousuario_id)
            cursor.execute(sql)
            db.connection.commit()
            return True
        except Exception as ex:
            raise Exception(ex)

    @classmethod
    def verificar_usuario_existente(cls, db, usuario):
        cursor = db.connection.cursor()
        sql = """SELECT 1
            FROM usuario
            WHERE usuario = %s"""
        try:
            cursor.execute(sql, (usuario,))
            return cursor.fetchone() is not None
        except Exception as ex:
            raise Exception(ex)