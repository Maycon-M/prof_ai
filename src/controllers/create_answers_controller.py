from fastapi import HTTPException

from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.create_answers_interface import ICreateAnswers

# LOGGER
from src.configs.logging_config import LOGGER

class CreateAnswersController(IController):
    """Controller responsável por criar respostas para uma prova.
    
    Attributes:
        __create_answers_service (ICreateAnswers): Serviço para manipulação de operações relacionadas às respostas.
    """
    
    def __init__(self, create_answers_service: ICreateAnswers) -> None:
        self.__service = create_answers_service
        self.logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para criar novas respostas.
        
        Args:
            request (HttpRequest): A requisição HTTP contendo os dados das respostas a serem criadas.
            
        Returns:
            HttpResponse: Resposta HTTP com o status e os dados das respostas criadas.
            
        Raises:
            HTTPException: Se ocorrer um erro específico relacionado à requisição.
            Exception: Para outros erros inesperados.
        """   
        try:
            answers_dto = request.body
            answers_data = await self.__service.execute(answers_dto)
            return HttpResponse(status_code=201, body=answers_data)
        
        except HTTPException as http_exc:
            self.logger.error(f"HTTP Exception: {http_exc.detail}")
            return http_exc
        
        except Exception as e:
            self.logger.error(f"Unexpected error: {str(e)}")
            return HttpResponse(status_code=500, body={"error": str(e)})
