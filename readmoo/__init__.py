from calibre.ebooks.metadata.sources.base import Source
from calibre_plugins.readmoo.main import ID_NAME, Book


class Readmoo(Source):
    name = "Readmoo"
    description = "Downloads metadata and covers from Readmoo"
    author = "Aphronyx So͘"
    version = (0, 0, 0)

    capabilities = frozenset({"cover"})

    def get_book_url(self, identifiers):  # pyright: ignore [reportIncompatibleMethodOverride]
        if id := identifiers.get(ID_NAME):
            return (ID_NAME, id, Book(id).url)

        if (isbn := identifiers.get("isbn")) and (books := Book.search(isbn)):
            return ("isbn", isbn, books[0].url)

        if (eisbn := identifiers.get("eisbn")) and (books := Book.search(eisbn)):
            return ("eisbn", eisbn, books[0].url)

        return None

    def get_book_url_name(self, idtype, idval, url):  # pyright: ignore [reportIncompatibleMethodOverride]
        if idtype == ID_NAME:
            return self.name

        if idtype == "isbn":
            return "ISBN"

        if idtype == "eisbn":
            return "eISBN"

    def get_cached_cover_url(self, identifiers):  # pyright: ignore [reportIncompatibleMethodOverride]
        if id := identifiers.get(ID_NAME):
            return Book(id).cover_url

        if (isbn := identifiers.get("isbn")) and (books := Book.search(isbn)):
            return books[0].cover_url

        if (eisbn := identifiers.get("eisbn")) and (books := Book.search(eisbn)):
            return books[0].cover_url

        return None
