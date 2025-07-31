from fastapi import HTTPException
from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.define_answers_score_interface import IDefineAnswersScore

# LOGGER
from src.configs.logging_config import LOGGER

class DefineAnswersScoreController(IController):
    """Controller responsável por definir a pontuação de uma resposta.
    
    Attributes:
        __service (IDefineAnswersScore): Serviço para manipulação de operações relacionadas à definição de pontuação de respostas.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, define_answers_score_service: IDefineAnswersScore) -> None:
        self.__service = define_answers_score_service
        self.__logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para definir a pontuação de uma resposta.
        
        Args:
            request (HttpRequest): A requisição HTTP contendo o ID da resposta e a pontuação.
        
        Returns:
            HttpResponse: Resposta HTTP com status 204 se a operação for bem-sucedida.
        
        Raises:
            HTTPException: Se ocorrer um erro ao definir a pontuação, retornando o status 404 ou 500.
        """
        try:
            answer_id = request.param.get('answer_id')
            score = request.param.get('score')
            await self.__service.execute(answer_id, score)
            return HttpResponse(status_code=204)
        
        except HTTPException as e:
            self.__logger.error(f"HTTPException: {e.status_code} - {e.detail}")
            raise e
        
        except Exception as e:
            self.__logger.error(f"Erro ao definir pontuação da resposta: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})
