from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.create_questions_interface import ICreateQuestionsService

# LOGGER
from src.configs.logging_config import LOGGER

class CreateQuestionsController(IController):
    """Controller responsável por criar questões associadas a uma prova.
    
    Attributes:
        __create_questions_service (ICreateQuestionsService): Serviço para manipulação de operações relacionadas às questões.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, create_questions_service: ICreateQuestionsService) -> None:
        self.__service = create_questions_service
        self.__logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para criar novas questões associadas a uma prova."""
        try:
            questions_dto = request.body
            exam_id = request.param.get('exam_id')
            questions_data = await self.__service.execute(questions_dto, exam_id)
            return HttpResponse(status_code=201, body=questions_data)
        except Exception as e:
            self.__logger.error(f"Erro ao criar questões: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})