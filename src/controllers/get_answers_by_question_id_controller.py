from fastapi import HTTPException
from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.get_answers_by_question_id_interface import IGetAnswersByQuestionId

# LOGGER
from src.configs.logging_config import LOGGER

class GetAnswersByQuestionIdController(IController):
    """Controller responsável por obter respostas associadas a um question_id específico.
    
    Attributes:
        __service (IGetAnswersByQuestionId): Serviço para manipulação de operações relacionadas às respostas.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, get_answers_service: IGetAnswersByQuestionId) -> None:
        self.__service = get_answers_service
        self.__logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para obter respostas por question_id.
        
        Args:
            request (HttpRequest): A requisição HTTP contendo o question_id.
        
        Returns:
            HttpResponse: Resposta HTTP com a lista de respostas associadas ao question_id.
        
        Raises:
            HTTPException: Se ocorrer um erro ao obter as respostas, retornando o status 404 ou 500.
        """
        try:
            question_id = request.param.get('question_id')
            answers_data = await self.__service.execute(question_id)
            return HttpResponse(status_code=200, body=answers_data)
        
        except HTTPException as e:
            self.__logger.error(f"HTTPException: {e.status_code} - {e.detail}")
            raise e
        
        except Exception as e:
            self.__logger.error(f"Erro ao obter respostas: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})
