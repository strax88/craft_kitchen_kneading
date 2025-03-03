from fastapi import HTTPException


class AsyncClientBaseHTTPException(HTTPException):

    status_code = 500
    detail = "AsyncClientBaseHTTPException"

    def __init__(self, status_code: int | None = None, detail: str | None = None):
        """"""
        self.status_code = status_code or self.status_code
        self.detail = detail or self.detail

