class Autor:

    def __init__(self, id, apellido, nombre, fechanacimiento=None):
        self.id = id
        self.apellido = apellido
        self.nombre = nombre
        self.fechanacimiento = fechanacimiento

    def nombre_completo(self):
        return "{0}, {1}".format(self.apellido, self.nombre)
