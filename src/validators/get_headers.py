from fastapi import Request

def get_request_headers(request: Request):
    return request.headers