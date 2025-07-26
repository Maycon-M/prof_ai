# INTERFACES
from src.interfaces.services.create_teacher_interface import ICreateTeacher
from src.interfaces.models.teachers_repository_interface import ITeachersRepository

# LOGGER
from src.configs.logging_config import LOGGER

# SCHEMAS
from src.schemas.teachers import Teacher

# SERVICE
from src.services.get_time_stamp import GetTimeStamp

# ERRORS
from src.errors.http_bad_request import HttpBadRequest
from src.errors.http_internal_server_error import HttpInternalServerError

class CreateTeacher(ICreateTeacher):
    
    """Serviço para criar um novo professor.
    
    Attributes:
        __teachers_repository (ITeachersRepository): Repositório de professores.
        __get_time_stamp (GetTimeStamp): Serviço para obter o timestamp atual.
        __logger (LOGGER): Logger para registrar eventos.
    """
    
    def __init__(self, teachers_repository: ITeachersRepository) -> None:
        self.__teachers_repository = teachers_repository
        self.__get_time_stamp = GetTimeStamp()
        self.__logger = LOGGER
        
    async def execute (self, teacher_dto: dict) -> dict:
        """Cria um novo professor com os dados fornecidos.
        Args:
            teacher_dto (dict): Um dicionário contendo as informações do professor.
        
        Returns:
            dict: Um dicionário contendo as informações do professor criado.
            
        Raises:
            HttpBadRequest: Se os dados do professor forem inválidos.
            HttpInternalServerError: Se ocorrer um erro ao inserir o professor no repositório.
        """
        
        created_at = self.__get_time_stamp.get_current_time_stamp()
        try:
            teacher_data = Teacher(
                name=teacher_dto.get("name"),
                email=teacher_dto.get("email"),
                created_at=created_at
            )
        except Exception as e:
            self.__logger.error(f"Erro ao criar objeto Teacher: {e}")
            raise HttpBadRequest("Dados inválidos para criar o professor.")
            
        try:
            self.__teachers_repository.create_teacher(teacher_data)
        
        except Exception as e:
            self.__logger.error(f"Erro ao criar professor: {e}")
            raise HttpInternalServerError("Erro ao criar professor.")
        
        return self.__format_response(teacher_data)
    
    def __format_response(self, teacher_data: Teacher) -> dict:
        """Formata a resposta do serviço."""
        return {
            "status": "success",
            "message": "Professor criado com sucesso.",
            "attributes": {
                "name": teacher_data.name,
                "email": teacher_data.email,
                "created_at": teacher_data.created_at.isoformat()
            }
        }
