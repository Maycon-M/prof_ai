from fastapi import HTTPException

class HttpBadRequest(HTTPException):
    def __init__(self, detail: str = "Bad request"):
        super().__init__(status_code=400, detail=detail)
        self.status_code = 400
        self.name = "Bad Request"
        self.detail = detail
