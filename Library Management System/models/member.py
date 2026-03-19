class Member:
    def __init__(self, name):
        self.name = name
        self.borrowed_books = []

    def __str__(self):
        return f"{self.name} - Borrowed Books: {len(self.borrowed_books)}"
        