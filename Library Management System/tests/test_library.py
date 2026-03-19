import pytest
from models.book import Book
from models.member import Member
from services.library import Library

@pytest.fixture
def library():
    lib = Library()
    lib.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    lib.add_book("To Kill a Mockingbird", "Harper Lee")
    lib.add_member("Alice")
    lib.add_member("Bob")
    return lib

def test_borrow_book(library):
    result = library.borrow_book("Alice", "The Great Gatsby")
    assert result == "Alice has borrowed 'The Great Gatsby'."
    assert not library.books[0].is_available
    assert library.members[0].borrowed_books[0].title == "The Great Gatsby"

def test_return_book(library):
    library.borrow_book("Alice", "The Great Gatsby")
    result = library.return_book("Alice", "The Great Gatsby")
    assert result == "Alice has returned 'The Great Gatsby'."
    assert library.books[0].is_available
    assert len(library.members[0].borrowed_books) == 0

def test_borrow_unavailable_book(library):
    library.borrow_book("Alice", "The Great Gatsby")
    result = library.borrow_book("Bob", "The Great Gatsby")
    assert result == "Book 'The Great Gatsby' is currently unavailable."    

def test_borrow_nonexistent_book(library):
    result = library.borrow_book("Alice", "Nonexistent Book")
    assert result == "Book 'Nonexistent Book' not found."

def test_borrow_nonexistent_member(library):
    result = library.borrow_book("Charlie", "The Great Gatsby")
    assert result == "Member 'Charlie' not found."

def test_return_nonexistent_book(library):
    result = library.return_book("Alice", "Nonexistent Book")
    assert result == "Book 'Nonexistent Book' not found."

def test_return_nonexistent_member(library):
    result = library.return_book("Charlie", "The Great Gatsby")
    assert result == "Member 'Charlie' not found."

def test_return_not_borrowed_book(library):
    result = library.return_book("Alice", "To Kill a Mockingbird")
    assert result == "Alice did not borrow 'To Kill a Mockingbird'."
