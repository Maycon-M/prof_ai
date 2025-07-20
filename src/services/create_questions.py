# LOGGER
from src.configs.logging_config import LOGGER

# INTERFACES
from src.interfaces.services.create_questions_interface import ICreateQuestionsService
from src.interfaces.models.questions_repository_interface import IQuestionsRepository

# SERVICES
from src.services.get_time_stamp import GetTimeStamp

class CreateQuestionsService (ICreateQuestionsService):
    
    """Classe responsável por criar questões associadas a uma prova.
    
    Attributes:
        __questions_repository (IQuestionsRepository): Repositório para manipulação de operações relacionadas às questões.
        __logger (Logger): Logger para registrar eventos e erros.
        __get_time_stamp (GetTimeStamp): Serviço para obter o timestamp atual.
    """
    
    def __init__(self, questions_repository: IQuestionsRepository) -> None:
        self.__questions_repository = questions_repository
        self.__logger = LOGGER
        self.__get_time_stamp = GetTimeStamp
        
    async def execute(self, questions_dto: dict, exam_id: int) -> dict:
        """Cria as novas questões recebidas no banco de dados.
        
        Args:
            questions_dto (dict): Dicionário contendo as questões a serem criadas.
            exam_id (int): ID da prova associada às questões.
            
        Returns:
            dict: Dicionário com o status da operação e mensagem de sucesso.
        """
        
        for question in questions_dto['questions']:
            question_data = {
                "text": question['question'],
                "number": question['number'],
                "exam_id": exam_id,
                "created_at": self.__get_time_stamp.get_current_time_stamp(),
                "correction_status": "Pendente"
            }
            self.__insert_question(question_data)
        
        return self.__format_response()
            
    def __insert_question(self, question_data: dict) -> None:
        """Insere a questão no repositório.
        
        Args:
            question_data (dict): Dicionário contendo os dados da questão a ser inserida.
        """
        try:
            self.__questions_repository.create_question(question_data)
        except Exception as e:
            self.__logger.error(f"Erro ao criar questão: {e}", exc_info=True, stack_info=True)
            raise e
    
    def __format_response(self) -> dict:
        """Formata a resposta da criação das questões.
        
        Returns:
            dict: Dicionário com o status da operação e mensagem de sucesso.
        """
        return {
            "status": "success",
            "message": "Questões criadas com sucesso."
        }
