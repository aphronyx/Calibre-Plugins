from calibre.ebooks.metadata.sources.base import Source
from calibre_plugins.readmoo.main import ID_NAME, Book


class Readmoo(Source):
    name = "Readmoo"
    description = "Downloads metadata and covers from Readmoo"
    author = "Aphronyx So͘"
    version = (0, 0, 0)

    def get_book_url(self, identifiers):
        if id := identifiers.get(ID_NAME):
            return (ID_NAME, id, Book(id).url)

        if (isbn := identifiers.get("isbn")) and (books := Book.search(isbn)):
            return ("isbn", isbn, books[0].url)
