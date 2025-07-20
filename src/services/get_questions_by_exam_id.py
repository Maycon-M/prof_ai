# INTERFACES
from src.interfaces.services.get_questions_by_exam_id_interface import IGetQuestionsByExamId
from src.interfaces.models.questions_repository_interface import IQuestionsRepository

# LOGGER
from src.configs.logging_config import LOGGER

# ERRORS
from src.errors.http_not_found import HttpNotFound

class GetQuestionsByExamId (IGetQuestionsByExamId):
    """Serviço para obter questões de um repositório."""
    
    def __init__(self, questions_repository: IQuestionsRepository) -> None:
        self.__questions_repository = questions_repository
        self.__logger = LOGGER
        
    async def execute (self, exam_id: int) -> dict:
        """Obtém todas as questões associadas a um exame específico.
        
        Args:
            exam_id (int): ID do exame para o qual as questões devem ser recuperadas.
        
        Returns:
            dict: Dicionário contendo as questões associadas ao exame.
        
        Raises:
            ValueError: Se não forem encontradas questões associadas ao exame fornecido.
            Exception: Se ocorrer um erro ao acessar o repositório de questões.  
        
        """
        try:
            questions = self.__questions_repository.get_questions_by_exam_id(exam_id) 
            
            if not questions:
                self.__logger.error(f"Nenhuma questão encontrada para o exame ID: {exam_id}", exc_info=True, stack_info=True)        
                raise HttpNotFound("Nenhuma questão encontrada para o exame fornecido.")
            
            return self.__format_response(questions)
        
        except Exception as e:
            self.__logger.error(f"Erro ao obter questões: {e}", exc_info=True, stack_info=True)
            raise e
        
    def __format_response(self, questions_data: list[dict]) -> dict:
        """Formata a resposta para o formato esperado."""
        
        questions = []
        
        for question in questions_data:
            question_dict = {
                'id': question.id,
                'number': question.question_number,
                'text': question.question_text,
                'correction_status': question.correction_status,
                'exam_id': question.exam_id,
                'created_at': question.created_at.isoformat()
            }
            questions.append(question_dict)
        
        response = {
            'questions': questions
        }
    
        return response
