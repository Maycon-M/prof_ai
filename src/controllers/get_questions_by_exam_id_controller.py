from fastapi import HTTPException
from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.get_questions_by_exam_id_interface import IGetQuestionsByExamId

# LOGGER
from src.configs.logging_config import LOGGER

class GetQuestionsByExamIdController(IController):
    """Controller responsável por obter questões associadas a uma prova.
    
    Attributes:
        __get_questions_service (IGetQuestions): Serviço para manipulação de operações relacionadas às questões.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, get_questions_service: IGetQuestionsByExamId) -> None:
        self.__service = get_questions_service
        self.__logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para obter questões associadas a uma prova."""
        try:
            exam_id = request.param.get('exam_id')
            questions_data = await self.__service.execute(exam_id)
            return HttpResponse(status_code=200, body=questions_data)
        
        except HTTPException as e:
            self.__logger.error(f"HTTPException: {e.status_code} - {e.detail}")
            raise e
        
        except Exception as e:
            self.__logger.error(f"Erro ao obter questões: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})
