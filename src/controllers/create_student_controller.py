from fastapi import HTTPException

from src.controllers.http_types.http_request import HttpRequest
from src.controllers.http_types.http_response import HttpResponse

# INTERFACES
from src.interfaces.controllers.controllers_interface import IController
from src.interfaces.services.create_student_interface import ICreateStudent

# LOGGER
from src.configs.logging_config import LOGGER

class CreateStudentController(IController):
    """Controller responsável por criar um aluno.
    
    Attributes:
        __service (ICreateStudent): Serviço para manipulação de operações relacionadas aos alunos.
        __logger (Logger): Logger para registrar eventos e erros.
        
    """
    
    def __init__(self, create_student_service: ICreateStudent) -> None:
        self.__service = create_student_service
        self.__logger = LOGGER

    async def handle(self, request: HttpRequest) -> HttpResponse:
        """Manipula a requisição para criar um novo aluno.
        
        Args:
            request (HttpRequest): A requisição HTTP contendo os dados do aluno.
        
        Returns:
            HttpResponse: Resposta HTTP com o status da criação do aluno.
        
        Raises:
            HTTPException: Se ocorrer um erro ao criar o aluno, retornando o status 400 ou 500.
        """
        try:
            student_dto = request.body
            student_data = await self.__service.execute(student_dto)
            return HttpResponse(status_code=201, body=student_data)
        except HTTPException as http_exc:
            self.__logger.error(f"Erro ao criar aluno: {http_exc.detail}", exc_info=True, stack_info=True)
            return http_exc
        
        except Exception as e:
            self.__logger.error(f"Erro ao criar aluno: {e}", exc_info=True, stack_info=True)
            return HttpResponse(status_code=500, body={"error": str(e)})
