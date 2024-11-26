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

    def test_cover_url(self) -> None:
        self.assertEqual(
            Book("210305007000101").cover_url,
            "https://cdn.readmoo.com/cover/pm/rnjkuhi.jpg",
        )

    def test_valid_url(self) -> None:
        self.assertIsInstance(
            Book.from_url("https://readmoo.com/book/210305007000101"), Book
        )

    def test_invalid_url(self) -> None:
        url = "invalid"

        with self.assertRaises(ValueError) as context:
            Book.from_url(url)

        self.assertEqual(str(context.exception), f"Invalid book URL: {url}")

    def test_categories(self) -> None:
        self.assertEqual(Book("210305007000101").tags, ["社會科學", "政治"])

    def test_title(self) -> None:
        self.assertEqual(
            Book("210305007000101").title,
            "時代如何轉了彎：蔡英文與臺灣轉型八年【附作者之一張惠菁親聲朗讀前言音檔】",
        )

    def test_rating(self) -> None:
        self.assertEqual(Book("210305007000101").rating, "4.8")

    def test_no_rating(self) -> None:
        self.assertIsNone(Book("210006079000101").rating)

    def test_authors(self) -> None:
        self.assertEqual(
            Book("210305007000101").authors, ["張惠菁", "吳錦勳", "李桐豪"]
        )

    def test_publisher(self) -> None:
        self.assertEqual(Book("210305007000101").publisher, "鏡文學股份有限公司")

    def test_publication_date(self) -> None:
        self.assertEqual(Book("210305007000101").publication_date, "2023/12/15")

    def test_language(self) -> None:
        self.assertEqual(Book("210305007000101").language, "繁體中文")

    def test_isbn(self) -> None:
        self.assertEqual(Book("210305007000101").isbn, "9786267229903")

    def test_no_isbn(self) -> None:
        self.assertIsNone(Book("210133088000101").isbn)

    def test_eisbn(self) -> None:
        self.assertEqual(Book("210305007000101").eisbn, "9786267229897")

    def test_no_eisbn(self) -> None:
        self.assertIsNone(Book("210133088000101").eisbn)

    def test_series(self) -> None:
        self.assertEqual(Book("210096256000101").series, "小書痴的下剋上")

    def test_no_series(self) -> None:
        self.assertIsNone(Book("210305007000101").series)

    def test_description(self) -> None:
        desc = Book("210305007000101").description

        self.assertTrue("採訪三十位幕僚、政務官、社會運動者等政策相關人士" in desc)
        self.assertTrue("這八年，是民主臺灣的「大規劃時代」" in desc)
