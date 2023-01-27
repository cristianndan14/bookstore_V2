class Book:

    def __init__(self, isbn, title, author, publication_date, price, cover):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.price = price
        self.cover = cover
        self.items_sold = 0
