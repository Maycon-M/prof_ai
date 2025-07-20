from fastapi import HTTPException

class HttpNotFound(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(status_code=404, detail=detail)
        self.status_code = 404
        self.name = "Not Found"
        self.detail = detail
