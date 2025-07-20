# INTERFACES
from src.interfaces.services.create_student_interface import ICreateStudentService
from src.interfaces.models.questions_repository_interface import IQuestionsRepository

# LOGGER
from src.configs.logging_config import LOGGER

# SERVICES
from src.services.get_time_stamp import GetTimeStamp

# SCHEMAS
from src.schemas.student import Student

# ERRORS
from src.errors.http_bad_request import HttpBadRequest
from src.errors.http_internal_server_error import HttpInternalServerError

class CreateStudent (ICreateStudentService):
    
    def __init__(self, questions_repository: IQuestionsRepository):
        self.__questions_repository = questions_repository
        self.__logger = LOGGER
        self.__get_time_stamp = GetTimeStamp()
        
    async def execute(self, student_dto: dict) -> dict:
        """Cria um novo aluno com os dados fornecidos.
        Args:
            student_dto (dict): Um dicionário contendo as informações do aluno.
            
        Returns:
            dict: Um dicionário contendo as informações do aluno criado.
        
        Raises:
            HttpBadRequest: Se os dados do aluno forem inválidos.
            HttpInternalServerError: Se ocorrer um erro ao inserir o aluno no repositório.
        """
        
        created_at = self.__get_time_stamp.get_current_time_stamp()
        
        try:
            student_data = Student(
                full_name=student_dto['full_name'],
                registration_number=student_dto['registration_number'],
                created_at=created_at
            )
        
        except Exception as e:
            self.__logger.error(f"Error creating student: {e}")
            raise HttpBadRequest(detail="Invalid student data provided")
    
        try:
            self.__insert_student(student_data)
        except Exception as e:
            raise e
    
        return self.__format_response(student_data)
    
    def __insert_student(self, student: Student):
        """Insere o aluno no repositório.
        Args:
            student (Student): O objeto Student a ser inserido.
            
        Raises:
            HttpInternalServerError: Se ocorrer um erro ao inserir o aluno no repositório.
        """
        
        try:
            self.__questions_repository.insert_student(student)
            self.__logger.info(f"Student {student.full_name} created successfully.")
        except Exception as e:
            self.__logger.error(f"Error inserting student into repository: {e}")

    
    def __format_response(self, student: Student) -> dict:
        
        """Formata a resposta da criação do aluno.
        Args:
            student (Student): O objeto Student criado.
        
        Returns:
            dict: Um dicionário formatado com os detalhes do aluno criado.
        """
        
        return {
            "status": "success",
            "message": "Aluno criado com sucesso.",
            "attributes": {
                "full_name": student.full_name,
                "registration_number": student.registration_number,
                "time_stamp": student.time_stamp.isoformat(),
            }
        }
