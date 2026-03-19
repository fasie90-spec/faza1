from models.book import Book
from models.member import Member
from services.library import Library

def main():
    library = Library()

    # Adding books
    library.add_book("The Great Gatsby", "F. Scott Fitzgerald")
    library.add_book("To Kill a Mockingbird", "Harper Lee")

    # Adding members
    library.add_member("Alice")
    library.add_member("Bob")

    # Borrowing books
    print(library.borrow_book("Alice", "The Great Gatsby"))
    print(library.borrow_book("Bob", "To Kill a Mockingbird"))

    # Listing books and members
    print("\nBooks in Library:")
    for book in library.list_books():
        print(book)

    print("\nLibrary Members:")
    for member in library.list_members():
        print(member)

if __name__ == "__main__":
    main()