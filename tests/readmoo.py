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
