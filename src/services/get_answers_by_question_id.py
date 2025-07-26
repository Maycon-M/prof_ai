# INTERFACES
from src.interfaces.services.get_answers_by_question_id_interface import IGetAnswersByQuestionId
from src.interfaces.models.answers_repository_interface import IAnswersRepository

# LOGGER
from src.configs.logging_config import LOGGER

# ERRORS
from src.errors.http_not_found import HttpNotFound
from src.errors.http_internal_server_error import HttpInternalServerError

class GetAnswersByQuestionId(IGetAnswersByQuestionId):
    
    """Serviço para obter respostas associadas a um question_id específico.
    
    Attributes:
        __answers_repository (IAnswersRepository): Repositório de respostas para acessar os dados.
        __logger (Logger): Logger para registrar eventos e erros.
    """
    
    def __init__(self, answers_repository: IAnswersRepository):
        self.__answers_repository = answers_repository
        self.__logger = LOGGER
        
    async def execute(self, question_id: int) -> dict:
        """Obtém todas as respostas associadas a um question_id específico.
        
        Args:
            question_id (int): ID da questão para a qual as respostas serão buscadas.
        
        Returns:
            dict: Dicionário contendo a lista de respostas associadas ao question_id.
        
        Raises:
            HttpNotFound: Se não forem encontradas respostas para o question_id fornecido.
            HttpInternalServerError: Se ocorrer um erro ao acessar o repositório de respostas.
        """
        try:
            answers = await self.__answers_repository.get_answers_by_question_id(question_id)
            if not answers:
                raise HttpNotFound(f"No answers found for question_id {question_id}")
            return self.__format_response(answers)
        except Exception as e:
            self.__logger.error(f"Error fetching answers for question_id {question_id}: {e}")
            raise HttpInternalServerError("An error occurred while fetching answers") from e
        
    def __format_response(self, answers: list) -> dict:
        
        formatted_answers = []
        
        for answer in answers:
            formatted_answers.append({
                "id": answer.id,
                "question_id": answer.question_id,
                "student_id": answer.student_id,
                "answer_text": answer.answer_text,
                "created_at": answer.created_at.isoformat(),
                "correction_status": answer.correction_status
            })
        
        return {"answers": formatted_answers}
