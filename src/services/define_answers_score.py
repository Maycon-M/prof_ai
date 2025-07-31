# INTERFACES
from src.interfaces.services.define_answers_score_interface import IDefineAnswersScore
from src.interfaces.models.answers_repository_interface import IAnswersRepository

# LOGGER
from src.configs.logging_config import LOGGER

# ERROS
from src.errors.http_not_found import HttpNotFound
from src.errors.http_bad_request import HttpBadRequest
from src.errors.http_internal_server_error import HttpInternalServerError

class DefineAnswersScore(IDefineAnswersScore):
    
    """Serviço para definir a pontuação de respostas.
    Arguments:
        __answers_repository (IAnswersRepository): Interface para o repositório de respostas.
        __logger (LOGGER): Logger para registrar eventos e erros.
    """
    
    def __init__(self, answers_repository: IAnswersRepository):
        self.__answers_repository = answers_repository
        self.__logger = LOGGER
        
    async def execute(self, answer_id: int, score: float) -> None:
        """Define a pontuação de uma resposta.
        
        Args:
            answer_id (int): ID da resposta cuja pontuação será definida.
            score (float): Pontuação a ser atribuída à resposta.
        
        Raises:
            HttpNotFound: Se a resposta não for encontrada.
            HttpBadRequest: Se a pontuação for inválida.
            HttpInternalServerError: Se ocorrer um erro ao atualizar a pontuação.
        """
        
        try:
            answer = await self.__answers_repository.get_answer_by_id(answer_id)
            if not answer:
                raise HttpNotFound(f"Resposta com ID {answer_id} não encontrada.")
            
            await self.__answers_repository.update_score(answer_id, score, "Corrigida")
        
        except ValueError as ve:
            self.__logger.error(f"Erro ao atualizar pontuação da resposta: {ve}")
            raise HttpBadRequest("Erro ao atualizar pontuação da resposta: %s", ve) from ve    
        
        except Exception as e:
            self.__logger.error(f"Erro ao definir pontuação da resposta: {e}")
            raise HttpInternalServerError("Erro ao atualizar a pontuação da resposta.") from e
