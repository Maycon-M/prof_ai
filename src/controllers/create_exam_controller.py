from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.create_exam_interface import ICreateExamService

class CreateExamController(IController):
    """Controller responsável por criar uma prova.
    
    Attributes:
        __create_exam_service (ICreateExamService): Serviço para manipulação de operações relacionadas às provas.
    """
    
    def __init__(self, create_exam_service: ICreateExamService) -> None:
        self.__service = create_exam_service

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para criar uma nova prova."""   
        try:
            exam_dto = request.body
            exam_data = await self.__service.execute(exam_dto)
            return HttpResponse(status_code=201, body=exam_data)
        except Exception as e:
            return HttpResponse(status_code=500, body={"error": str(e)})
