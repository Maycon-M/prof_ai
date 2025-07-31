
class HttpRequest:
    """
    Classe que define com deve ser um request de http
    """
    def __init__(self, body: dict = None, param: dict = None, headers: dict = None, token_infos: dict = None) -> None:
        self.body = body
        self.param = param
        self.headers = headers
