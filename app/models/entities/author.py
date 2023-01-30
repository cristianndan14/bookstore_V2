class Author:

    def __init__(self, id_author, name, last_name, birth_date=None):
        self.id_author = id_author
        self.name = name
        self.last_name = last_name
        self.birth_date = birth_date

    def full_name(self):
        return "{0}, {1}".format(self.last_name, self.name)
