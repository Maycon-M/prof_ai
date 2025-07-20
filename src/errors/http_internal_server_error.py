from fastapi import HTTPException

class HttpInternalServerError(HTTPException):
    def __init__(self, detail: str = "Internal server error"):
        super().__init__(status_code=500, detail=detail)
        self.status_code = 500
        self.name = "Internal Server Error"
        self.detail = detail