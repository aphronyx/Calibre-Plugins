from operator import itemgetter
from threading import Thread
from typing import Self

import requests
from lxml import html

ID_NAME: str = "readmoo"


class Book:
    def __init__(self, id: str, timeout: int | None = None) -> None:
        url = f"{self.__DOMAIN}/book/{id}"
        res = requests.get(url, timeout=timeout)
        res_status = res.status_code
        if res_status == 404:
            raise ValueError(f"Invalid ID: {id}")

        if not res.ok:
            raise Exception(
                f"Unsuccessful response for ID: {id}\n"
                f"Reason: {res_status} {res.reason}"
            )

        self.__id = id
        self.__url = url
        self.__webpage = html.fromstring(res.text)

    @classmethod
    def search(cls, keyword: str, timeout: int | None = None) -> list[Self]:
        url = f"{cls.__DOMAIN}/search/keyword?q={keyword}&page=1&st=true"
        res = requests.get(url, timeout=timeout).text
        ids = html.fromstring(res).xpath("//a[@class='product-link']/@data-readmoo-id")
        max = ids_len if (ids_len := len(ids)) < 20 else 20

        results = []
        threads = []
        for index, id in enumerate(ids[:max]):
            thread = Thread(target=cls.__append_to, args=(index, id, results, timeout))
            thread.start()
            threads.append(thread)
        [thread.join() for thread in threads]

        books = [book for _, book in sorted(results, key=itemgetter(0))]
        return books

    @property
    def id(self) -> str:
        return self.__id

    @property
    def url(self) -> str:
        return self.__url

    @property
    def cover_url(self) -> str:
        try:
            return (
                self.__webpage.xpath("//div[@class='cover-img text-center']/img/@src")[
                    0
                ]
                .rsplit("?", 1)[0]
                .replace("_460x580", "")
            )

        except Exception as e:
            raise Exception(
                f"Failed to scrape cover URL for ID: {self.__id}\n" f"Reason: {e}"
            )

    __DOMAIN: str = "https://readmoo.com"

    @classmethod
    def __append_to(
        cls,
        index: int,
        id: str,
        results: list[tuple[int, Self]],
        timeout: int | None = None,
    ) -> None:
        results.append((index, cls(id, timeout)))
