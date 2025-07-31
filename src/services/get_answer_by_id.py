# INTERFACES
from src.interfaces.services.get_answer_by_id_interface import IGetAnswerById
from src.interfaces.models.answers_repository_interface import IAnswersRepository

# LOGGER
from src.configs.logging_config import LOGGER

# ERRORS
from src.errors.http_not_found import HttpNotFound
from src.errors.http_internal_server_error import HttpInternalServerError

class GetAnswerById(IGetAnswerById):
    """Serviço para obter uma resposta pelo ID de um repositório de respostas.
    
    Arguments:
        __answers_repository (IAnswersRepository): Interface para o repositório de respostas.
        __logger (LOGGER): Logger para registrar eventos e erros.
    """
    
    def __init__(self, answers_repository: IAnswersRepository) -> None:
        self.__answers_repository = answers_repository
        self.__logger = LOGGER
        
        
    async def execute(self, answer_id: int) -> dict:
        """Obtém uma resposta pelo ID.
        
        Args:
            answer_id (int): ID da resposta a ser recuperada.
        
        Returns:
            dict: Dicionário contendo os dados da resposta.
        
        Raises:
            ValueError: Se o ID da resposta não for encontrado.
            Exception: Se ocorrer um erro ao acessar o repositório de respostas.
        """
        
        try:
            answer = await self.__answers_repository.get_answer_by_id(answer_id)
            
            if not answer:
                self.__logger.error(f"Resposta com ID {answer_id} não encontrada.")
                raise HttpNotFound(f"Resposta com ID {answer_id} não encontrada.")
            
            return self.__format_response(answer)
        
        except Exception as e:
            self.__logger.error(f"Erro ao obter resposta: {e}", exc_info=True, stack_info=True)
            raise HttpInternalServerError("Erro interno ao obter a resposta.") from e
    
    def __format_response(self, answer_data) -> dict:
        """Formata a resposta para o formato esperado."""
        
        return {
            'id': answer_data.id,
            'question_id': answer_data.question_id,
            'student_id': answer_data.student_id,
            'answer_text': answer_data.answer_text,
            'created_at': answer_data.created_at.isoformat(),
            'correction_status': answer_data.correction_status
        }
