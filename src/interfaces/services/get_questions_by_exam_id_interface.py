from abc import ABC, abstractmethod

class IGetQuestionsByExamId(ABC):
    """Classe Interface para obter questões de um serviço."""
    
    @abstractmethod
    async def execute(self, exam_id: int) -> list[dict]:
        """Obtém todas as questões associadas a um exame específico."""
        pass
