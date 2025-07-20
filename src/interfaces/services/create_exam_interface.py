from abc import ABC, abstractmethod

class ICreateExamService(ABC):
    """Classe Interface para o serviço de criação de provas."""
    
    @abstractmethod
    async def execute (self, exam_data: dict) -> dict:
        pass
