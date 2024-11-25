from unittest import TestCase

from . import import_from_path

main = import_from_path("main", "readmoo/main.py")
from main import Book  # pyright: ignore # noqa


class TestBook(TestCase):
    def test_valid_id(self) -> None:
        self.assertIsInstance(Book("210305007000101"), Book)

    def test_invalid_id(self) -> None:
        id = "invalid"

        with self.assertRaises(ValueError) as context:
            Book(id)

        self.assertEqual(str(context.exception), f"Invalid ID: {id}")

    def test_url(self) -> None:
        id = "210305007000101"

        self.assertEqual(Book(id).url, f"https://readmoo.com/book/{id}")

    def test_search_by_keyword(self) -> None:
        expected = [
            "290305214000101",
            "210305007000101",
            "210327431000101",
            "210151993000101",
            "210169924000101",
            "210327452000101",
            "210004400000101",
            "210355874000101",
            "210225629000101",
            "210133438000101",
            "210188083000101",
            "210163830000101",
            "210346931000101",
            "210088159000101",
            "210312649000101",
            "210337462000101",
            "220139496000101",
            "210354142000101",
            "210350346000101",
            "210051998000101",
        ]

        self.assertEqual([book.id for book in Book.search("時代如何轉了彎")], expected)

    def test_search_by_real_isbn(self) -> None:
        books = Book.search("9786267229903")

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].id, "210305007000101")

    def test_search_by_fake_isbn(self) -> None:
        self.assertFalse(Book.search("9784531372638"))

    def test_search_by_eisbn(self) -> None:
        books = Book.search("9786267229897")

        self.assertEqual(len(books), 1)
        self.assertEqual(books[0].id, "210305007000101")
