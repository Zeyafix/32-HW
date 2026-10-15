def create_books():
    return [
        {"id": "b01", "title": "The Hobbit", "author": "J. R. R. Tolkien", "total": 3},
        {"id": "b02", "title": "Dune", "author": "Frank Herbert", "total": 2},
        {"id": "b03", "title": "Fahrenheit 451", "author": "Ray Bradbury", "total": 1},
        {"id": "b04", "title": "The Little Prince", "author": "Antoine de Saint-Exupery", "total": 2},
    ]


def find_book(books, book_id):
    for book in books:
        if book["id"] == book_id:
            return book
    return None


def search_books(books, query):
    query = query.strip().lower()
    return [
        book for book in books
        if query in book["title"].lower() or query in book["author"].lower()
    ]


def count_book_loans(loans, book_id):
    return sum(1 for loan in loans if loan["book_id"] == book_id)


def get_available_count(book, loans):
    return book["total"] - count_book_loans(loans, book["id"])


def find_loan(loans, book_id, reader):
    for loan in loans:
        if loan["book_id"] == book_id and loan["reader"] == reader:
            return loan
    return None


def borrow_book(books, loans, book_id, reader):
    book = find_book(books, book_id)
    if book is None:
        return "Book not found."
    if find_loan(loans, book_id, reader) is not None:
        return "This reader already has this book."
    if get_available_count(book, loans) == 0:
        return "No copies available."
    loans.append({"book_id": book_id, "reader": reader})
    return "Book issued."


def return_book(loans, book_id, reader):
    loan = find_loan(loans, book_id, reader)
    if loan is None:
        return "Loan not found."
    loans.remove(loan)
    return "Book returned."


def get_reader_loans(loans, reader):
    return [loan for loan in loans if loan["reader"] == reader]


def get_statistics(books, loans):
    total = sum(book["total"] for book in books)
    return {
        "titles": len(books),
        "copies": total,
        "borrowed": len(loans),
        "available": total - len(loans),
        "readers": len({loan["reader"] for loan in loans}),
    }


def format_book(book, loans):
    available = get_available_count(book, loans)
    return f"{book['id']} | {book['title']} | {book['author']} | {available} / {book['total']}"


def format_loan(loan, books):
    book = find_book(books, loan["book_id"])
    return f"{loan['book_id']} | {book['title']} | {loan['reader']}"


def show_books(books, loans):
    print("Books (ID | Title | Author | Available / Total):")
    if not books:
        print("No books found.")
    for book in books:
        print(format_book(book, loans))


def show_loans(loans, books):
    print("Loans (Book ID | Title | Reader):")
    if not loans:
        print("No active loans.")
    for loan in loans:
        print(format_loan(loan, books))


def show_statistics(books, loans):
    statistics = get_statistics(books, loans)
    print("Library statistics:")
    print(f"Titles: {statistics['titles']}")
    print(f"Copies: {statistics['copies']}")
    print(f"Borrowed: {statistics['borrowed']}")
    print(f"Available: {statistics['available']}")
    print(f"Readers: {statistics['readers']}")


def read_nonempty(prompt):
    value = input(prompt).strip()
    while not value:
        print("Please enter a non-empty value.")
        value = input(prompt).strip()
    return value


def search_action(books, loans):
    query = read_nonempty("Enter a title or author to search for: ")
    show_books(search_books(books, query), loans)


def borrow_action(books, loans):
    book_id = read_nonempty("Enter a book ID: ")
    reader = read_nonempty("Enter a reader name: ")
    print(borrow_book(books, loans, book_id, reader))


def return_action(loans):
    book_id = read_nonempty("Enter a book ID: ")
    reader = read_nonempty("Enter a reader name: ")
    print(return_book(loans, book_id, reader))


def reader_action(books, loans):
    reader = read_nonempty("Enter a reader name: ")
    show_loans(get_reader_loans(loans, reader), books)


def show_menu():
    print("\nLibrary menu:")
    print("1. Show all books")
    print("2. Search books")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. Show reader loans")
    print("6. Show all loans")
    print("7. Show statistics")
    print("0. Exit")


def main():
    books = create_books()
    loans = []
    while True:
        show_menu()
        choice = input("Choose an action (0-7): ").strip()
        if choice == "1":
            show_books(books, loans)
        elif choice == "2":
            search_action(books, loans)
        elif choice == "3":
            borrow_action(books, loans)
        elif choice == "4":
            return_action(loans)
        elif choice == "5":
            reader_action(books, loans)
        elif choice == "6":
            show_loans(loans, books)
        elif choice == "7":
            show_statistics(books, loans)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Unknown action. Choose a number from 0 to 7.")


if __name__ == "__main__":
    main()
