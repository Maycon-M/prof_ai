# INTERFACES
from src.interfaces.services.create_answers_interface import ICreateAnswers
from src.models.repositories.answers_repository import IAnswersRepository

# LOGGER
from src.configs.logging_config import LOGGER

# SERVICES
from src.services.get_time_stamp import GetTimeStamp

# ERRORS
from src.errors.http_internal_server_error import HttpInternalServerError

class CreateAnswers (ICreateAnswers):
    
    """Classe responsável por criar respostas associadas a questões.
    
    Attributes:
        __answers_repository (IAnswersRepository): Repositório para manipulação de operações relacionadas às respostas.
        __logger (Logger): Logger para registrar eventos e erros.
        __get_time_stamp (GetTimeStamp): Serviço para obter o timestamp atual.
    """
    
    def __init__(self, answers_repository: IAnswersRepository) -> None:
        self.__answers_repository = answers_repository
        self.__logger = LOGGER
        self.__get_time_stamp = GetTimeStamp()
        
    async def execute (self, answers_dto: dict) -> dict:
        
        """
        Cria as novas respostas recebidas no banco de dados.
        
        Args:
            answers_dto (dict): Dicionário contendo as respostas a serem criadas.
        
        Returns:
            dict: Dicionário com o status da operação e mensagem de sucesso.
        
        Raises:
            HttpInternalServerError: Se ocorrer um erro ao criar as respostas.
        """
        
        for answer in answers_dto['answers']:
            answer_data = {
                "question_id": answer['question_id'],
                "student_id": answer['student_id'],
                "answer_text": answer['answer_text'],
                "created_at": self.__get_time_stamp.get_current_time_stamp(),
                "correction_status": "Pendente"
            }
            try:
                await self.__insert_answer(answer_data)
            except Exception as e:
                self.__logger.error(f"Erro ao criar resposta: {e}", exc_info=True, stack_info=True)
                raise e
        
        return self.__format_response()
        
    async def __insert_answer(self, answer_data: dict) -> None:
        """Insere a resposta no repositório.
        
        Args:
            answer_data (dict): Dicionário contendo os dados da resposta a ser inserida.
            
        Raises:
            HttpInternalServerError: Se ocorrer um erro ao inserir a resposta no repositório.
        """
        try:
            await self.__answers_repository.insert_answer(answer_data)
        except Exception as e:
            self.__logger.error(f"Erro ao criar resposta: {e}", exc_info=True, stack_info=True)
            raise HttpInternalServerError(f"Erro ao criar resposta: {e}", exc_info=True, stack_info=True)
    
    def __format_response(self) -> dict:
        """Formata a resposta de sucesso.
        
        Returns:
            dict: Dicionário com o status e mensagem de sucesso.
        """
        return {
            "status": "success",
            "message": "Respostas criadas com sucesso."
        }
