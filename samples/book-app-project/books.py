import json
from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional

DATA_FILE = "data.json"


@dataclass
class Book:
    title: str
    author: str
    year: int
    read: bool = False


def get_book_stats(books: List[Book]) -> Dict[str, Any]:
    """Return basic statistics for a list of books."""
    if not books:
        return {
            "total_count": 0,
            "number_read": 0,
            "number_unread": 0,
            "oldest_book": None,
            "newest_book": None,
        }

    number_read = sum(1 for book in books if book.read)

    return {
        "total_count": len(books),
        "number_read": number_read,
        "number_unread": len(books) - number_read,
        "oldest_book": min(books, key=lambda book: book.year),
        "newest_book": max(books, key=lambda book: book.year),
    }


class BookCollection:
    def __init__(self):
        self.books: List[Book] = []
        self.load_books()

    def load_books(self):
        """Load books from the JSON file if it exists."""
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.books = [Book(**b) for b in data]
        except FileNotFoundError:
            self.books = []
        except json.JSONDecodeError:
            print("Warning: data.json is corrupted. Starting with empty collection.")
            self.books = []

    def save_books(self):
        """Save the current book collection to JSON."""
        with open(DATA_FILE, "w") as f:
            json.dump([asdict(b) for b in self.books], f, indent=2)

    def add_book(self, title: str, author: str, year: int) -> Book:
        book = Book(title=title, author=author, year=year)
        self.books.append(book)
        self.save_books()
        return book

    def list_books(self) -> List[Book]:
        return self.books

    def find_book_by_title(self, title: str) -> Optional[Book]:
        for book in self.books:
            if book.title.lower() == title.lower():
                return book
        return None

    def mark_as_read(self, title: str) -> bool:
        book = self.find_book_by_title(title)
        if book:
            book.read = True
            self.save_books()
            return True
        return False

    def remove_book(self, title: str) -> bool:
        """Remove a book by title."""
        book = self.find_book_by_title(title)
        if book:
            self.books.remove(book)
            self.save_books()
            return True
        return False

    def find_by_author(self, author: str) -> List[Book]:
        """Find all books by a given author."""
        return [b for b in self.books if b.author.lower() == author.lower()]
