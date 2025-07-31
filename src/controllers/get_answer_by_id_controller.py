from fastapi import HTTPException
from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.get_answer_by_id_interface import IGetAnswerById

# LOGGER
from src.configs.logging_config import LOGGER

class GetAnswerByIdController(IController):
    
    def __init__(self, get_answer_service: IGetAnswerById) -> None:
        self.__service = get_answer_service
        self.__logger = LOGGER
    
    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para obter uma resposta pelo ID.
        
        Args:
            request (HttpRequest): A requisição HTTP contendo o ID da resposta.
        
        Returns:
            HttpResponse: Resposta HTTP com os dados da resposta.
        
        Raises:
            HTTPException: Se ocorrer um erro ao obter a resposta, retornando o status 404 ou 500.
        """
        try:
            answer_id = request.param.get('answer_id')
            answer_data = await self.__service.execute(answer_id)
            return HttpResponse(status_code=200, body=answer_data)
        
        except HTTPException as e:
            self.__logger.error(f"HTTPException: {e.status_code} - {e.detail}")
            raise e
        
        except Exception as e:
            self.__logger.error(f"Erro ao obter resposta: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})
