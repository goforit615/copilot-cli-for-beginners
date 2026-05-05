import sys
from books import BookCollection, get_book_stats


# Global collection instance
collection = BookCollection()


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_stats():
    stats = get_book_stats(collection.list_books())

    print("\nBook Statistics\n")
    print(f"Total books: {stats['total_count']}")
    print(f"Read books: {stats['number_read']}")
    print(f"Unread books: {stats['number_unread']}")

    if stats["oldest_book"] is not None:
        oldest = stats["oldest_book"]
        print(f"Oldest book: {oldest.title} ({oldest.year})")
    else:
        print("Oldest book: None")

    if stats["newest_book"] is not None:
        newest = stats["newest_book"]
        print(f"Newest book: {newest.title} ({newest.year})")
    else:
        print("Newest book: None")

    print()


def show_help():
    print("""
Book Collection Helper

Commands:
  list     - Show all books
  add      - Add a new book
  remove   - Remove a book by title
  find     - Find books by author
    stats    - Show collection statistics
  help     - Show this help message
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "stats":
        handle_stats()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
