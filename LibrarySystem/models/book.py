class Book:
    def __init__(self, titlu: str, autor: str, isbn: str):
        self.este_imprumutata = False
        self.titlu = titlu
        self.autor = autor
        self.isbn = isbn