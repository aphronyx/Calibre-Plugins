import requests

ID_NAME: str = "readmoo"


class Book:
    def __init__(self, id: str) -> None:
        res = requests.get(f"https://readmoo.com/book/{id}")
        res_status = res.status_code
        if res_status == 404:
            raise ValueError(f"Invalid ID: {id}")

        if not res.ok:
            raise Exception(
                f"Unsuccessful response for ID: {id}\n"
                f"Reason: {res_status} {res.reason}"
            )
