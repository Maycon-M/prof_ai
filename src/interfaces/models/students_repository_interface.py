from abc import ABC, abstractmethod

# TABELA
from src.models.entities.students import StudentTable

# SCHEMA
from src.schemas.student import Student

class IStudentsRepository(ABC):
    """Classe Interface para o repositório de estudantes."""

    @abstractmethod
    def create_student(self, student_data: Student) -> None:
        """Cria um novo estudante no banco de dados."""
        pass

    @abstractmethod
    def get_student_by_registration_number(self, registration_number: str) -> StudentTable | None:
        """Retorna um estudante pelo número de matrícula."""
        pass
            
    @abstractmethod        
    def get_all_students(self) -> list[StudentTable]:
        """Retorna todos os estudantes cadastrados."""
        pass
    
    @abstractmethod
    def get_student_by_id(self, student_id: int) -> StudentTable | None:
        """Retorna um estudante pelo ID."""
        pass
