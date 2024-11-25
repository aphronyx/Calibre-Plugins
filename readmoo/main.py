import requests

ID_NAME: str = "readmoo"


class Book:
    def __init__(self, id: str) -> None:
        url = f"https://readmoo.com/book/{id}"
        res = requests.get(url)
        res_status = res.status_code
        if res_status == 404:
            raise ValueError(f"Invalid ID: {id}")

        if not res.ok:
            raise Exception(
                f"Unsuccessful response for ID: {id}\n"
                f"Reason: {res_status} {res.reason}"
            )

        self.__url = url

    @property
    def url(self) -> str:
        return self.__url
