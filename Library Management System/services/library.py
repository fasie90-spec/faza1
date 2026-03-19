from models.member import Member
from models.book import Book

class Library:
    def __init__(self):
        self.books = []
        self.members = []

    def add_book(self, title, author):
        book = Book(title, author)
        self.books.append(book)

    def add_member(self, name):
        member = Member(name)
        self.members.append(member)

    def borrow_book(self, member_name, book_title):
        member = next((m for m in self.members if m.name == member_name), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if member and book and book.is_available:
            member.borrowed_books.append(book)
            book.is_available = False
            return f"{member_name} has borrowed '{book_title}'."
        elif not member:
            return f"Member '{member_name}' not found."
        elif not book:
            return f"Book '{book_title}' not found."
        else:
            return f"Book '{book_title}' is currently unavailable."
        
    def return_book(self, member_name, book_title):
        member = next((m for m in self.members if m.name == member_name), None)
        book = next((b for b in self.books if b.title == book_title), None)

        if member and book and book in member.borrowed_books:
            member.borrowed_books.remove(book)
            book.is_available = True
            return f"{member_name} has returned '{book_title}'."
        elif not member:
            return f"Member '{member_name}' not found."
        elif not book:
            return f"Book '{book_title}' not found."
        else:
            return f"{member_name} did not borrow '{book_title}'."
        
    def list_books(self):
        return [str(book) for book in self.books]

    def list_members(self):
        return [str(member) for member in self.members]