from abc import ABC, abstractmethod

class IQuestionsRepository(ABC):
    """Classe Interface para o repositório de questões."""
    
    @abstractmethod
    def create_question(self, question_data: dict) -> None:
        """Cria uma nova questão no banco de dados."""
        pass
