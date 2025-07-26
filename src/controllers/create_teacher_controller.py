from fastapi import HTTPException

from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.create_teacher_interface import ICreateTeacher

# LOGGER
from src.configs.logging_config import LOGGER

class CreateTeacherController(IController):
    """Controller responsável por criar um professor.
    
    Attributes:
        __service (ICreateTeacher): Serviço para manipulação de operações relacionadas aos professores.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, create_teacher_service: ICreateTeacher) -> None:
        self.__service = create_teacher_service
        self.__logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para criar um novo professor.
        
        Args:
            request (HttpRequest): A requisição HTTP contendo os dados do professor.
        
        Returns:
            HttpResponse: Resposta HTTP com o status da criação do professor.
        
        Raises:
            HTTPException: Se ocorrer um erro ao criar o professor, retornando o status 400 ou 500.
        """
        try:
            teacher_dto = request.body
            teacher_data = await self.__service.execute(teacher_dto)
            return HttpResponse(status_code=201, body=teacher_data)
        
        except HTTPException as http_exc:
            self.__logger.error(f"Erro ao criar professor: {http_exc.detail}", exc_info=True, stack_info=True)
            return http_exc
        
        except Exception as e:
            self.__logger.error(f"Erro ao criar professor: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})
