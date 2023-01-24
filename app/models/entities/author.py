class Author:

    def __init__(self, id, last_name, name, birth_date=None):
        self.id = id
        self.last_name = last_name
        self.name = name
        self.birth_date = birth_date

    def full_name(self):
        return "{0}, {1}".format(self.last_name, self.name)
