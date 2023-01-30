class Book:

    def __init__(self, isbn, title, id_author, publication_date, price, cover):
        self.isbn = isbn
        self.title = title
        self.id_author = id_author
        self.publication_date = publication_date
        self.price = price
        self.cover = cover
        self.items_sold = 0
