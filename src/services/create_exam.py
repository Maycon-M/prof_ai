# LOGGER
from src.configs.logging_config import LOGGER

# INTERFACES
from src.interfaces.services.create_exam_interface import ICreateExamService
from src.interfaces.models.exams_repository_interface import IExamsRepository

# SCHEMAS
from src.schemas.exam import Exam

class CreateExam (ICreateExamService):
    
    """Classe responsável por criar uma prova.
    
    Attributes:
        __exams_repository (IExamsRepository): Repositório para manipulação de operações relacionadas às provas.
        __logger (Logger): Logger para registrar eventos e erros.
    
    """
    
    def __init__(self, exams_repository: IExamsRepository) -> None:
        self.__exams_repository = exams_repository
        self.__logger = LOGGER

    async def execute(self, exam_dto: dict) -> dict:
        """Cria uma nova prova no banco de dados."""
        
        time_stamp = self.__get_time_stamp()
        correction_status = "Pendente"
        
        exam_data = Exam(
            subject=exam_dto.subject,
            teacher_id=exam_dto.teacher_id,
            time_stamp=time_stamp,
            correction_status=correction_status
        )
        
        self.__insert_exam(exam_data)
        
        return self.__format_response(exam_data)
        
    def __get_time_stamp(self) -> str:
        """Obtém o timestamp atual."""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __insert_exam(self, exam_data: Exam) -> None:
        """Insere a prova no repositório."""
        try:
            self.__exams_repository.create_exam(exam_data)
            self.__logger.info("Prova criada com sucesso.")
        except Exception as e:
            self.__logger.error(f"Erro ao criar prova: {e}", exc_info=True, stack_info=True)
            raise e
        
    def __format_response(self, exam_data: Exam) -> dict:
        """Formata a resposta da criação da prova."""
        return {
            "status": "success",
            "message": "Prova criada com sucesso.",
            "attributes": {
                "subject": exam_data.subject,
                "teacher_id": exam_data.teacher_id,
                "time_stamp": exam_data.time_stamp.isoformat(),
                "correction_status": exam_data.correction_status
            }
        }
