from abc import ABC, abstractmethod

from src.schemas.exam import Exam

class IExamsRepository(ABC):
    """Classe Interface para o repositório de exames."""
    
    @abstractmethod
    def create_exam(self, exam_data: Exam) -> None:
        pass
