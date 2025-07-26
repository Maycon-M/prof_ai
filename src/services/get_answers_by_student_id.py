# INTERFACES
from src.interfaces.services.get_answers_by_student_id_interface import IGetAnswersByStudentId
from src.interfaces.models.answers_repository_interface import IAnswersRepository

# LOGGER
from src.configs.logging_config import LOGGER

# ERRORS
from src.errors.http_not_found import HttpNotFound
from src.errors.http_internal_server_error import HttpInternalServerError

class GetAnswersByStudentId(IGetAnswersByStudentId):
    """Serviço para obter respostas de um estudante pelo ID do estudante.
    
    Attributes:
        __answers_repository (IAnswersRepository): Repositório de respostas para acessar os dados.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, answers_repository: IAnswersRepository):
        self.__answers_repository = answers_repository
        self.__logger = LOGGER
        
    async def execute(self, student_id: int) -> dict:
        """Obtém todas as respostas de um estudante pelo ID do estudante.
        
        Args:
            student_id (int): ID do estudante cujas respostas serão recuperadas.
        
        Returns:
            dict: Dicionário contendo a lista de respostas do estudante.
        
        Raises:
            HttpNotFound: Se não forem encontradas respostas para o estudante.
            HttpInternalServerError: Se ocorrer um erro ao acessar o repositório de respostas.
        """
        try:
            answers = await self.__answers_repository.get_all_answers()
            student_answers = [answer for answer in answers if answer.student_id == student_id]
            
            if not student_answers:
                raise HttpNotFound(f"No answers found for student with ID {student_id}.")
            
            return self.__format_response(student_answers)
        
        except Exception as e:
            self.__logger.error(f"Error retrieving answers for student {student_id}: {e}")
            raise HttpInternalServerError("An error occurred while retrieving answers.")
    
    def __format_response(self, answers: list) -> dict:
        """Formata a resposta para o formato esperado.
        
        Args:
            answers (list): Lista de respostas do estudante.
        
        Returns:
            dict: Dicionário formatado com as respostas.
        """
        
        formatted_answers = [
            {
                "id": answer.id,
                "question_id": answer.question_id,
                "student_id": answer.student_id,
                "answer_text": answer.answer_text,
                "created_at": answer.created_at.isoformat(),
                "correction_status": answer.correction_status
            } for answer in answers
        ]
        
        return {"answers": formatted_answers}
