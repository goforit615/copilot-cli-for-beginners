import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection, get_book_stats


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


def test_get_book_stats_empty():
    stats = get_book_stats([])
    assert stats["total_count"] == 0
    assert stats["number_read"] == 0
    assert stats["number_unread"] == 0
    assert stats["oldest_book"] is None
    assert stats["newest_book"] is None


def test_get_book_stats_values():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    collection.add_book("Dune", "Frank Herbert", 1965)
    collection.add_book("Project Hail Mary", "Andy Weir", 2021)
    collection.mark_as_read("Dune")

    stats = get_book_stats(collection.list_books())

    assert stats["total_count"] == 3
    assert stats["number_read"] == 1
    assert stats["number_unread"] == 2
    assert stats["oldest_book"].title == "The Hobbit"
    assert stats["newest_book"].title == "Project Hail Mary"

# from typing import List, Dict, Optional, Any
    
# def get_book_stats(books: List[Book]) -> Dict[str, Any]:
#     """
#     Calculates statistics from a list of Book objects.
#     Returns a dictionary with counts and book objects.
#     """
#     if not books:
#         return {
#         "total_count": 0,
#         "number_read": 0,
#         "number_unread": 0,
#         "oldest_book": None,
#         "newest_book": None
#     }

#     total_count = len(books)
#     number_read = sum(1 for book in books if book.read)
#     number_unread = total_count - number_read

#     # Find books with min and max years
#     # min/max will return the first book encountered if there is a tie
#     oldest_book = min(books, key=lambda b: b.year)
#     newest_book = max(books, key=lambda b: b.year)

#     return {
#         "total_count": total_count,
#         "number_read": number_read,
#         "number_unread": number_unread,
#         "oldest_book": oldest_book,
#         "newest_book": newest_book
#     }
   
# --- Example Usage ---
# stats = get_book_stats(collection.list_books())
# print(f"Total: {stats['total_count']}")
# print(f"Oldest: {stats['oldest_book'].title} ({stats['oldest_book'].year})")