from abc import ABC, abstractmethod

# TABELA
from src.models.entities.questions import QuestionsTable

class IQuestionsRepository(ABC):
    """Classe Interface para o repositório de questões."""
    
    @abstractmethod
    def create_question(self, question_data: dict) -> None:
        """Cria uma nova questão no banco de dados."""
        pass
    
    @abstractmethod
    def get_questions_by_exam_id(self, exam_id: int) -> list[QuestionsTable]:
        """Retorna todas as questões associadas a uma prova específico."""
        pass
