from abc import ABC, abstractmethod

# TABELA
from src.models.entities.teachers import TeacherTable

# SCHEMA
from src.schemas.teachers import Teacher

class ITeachersRepository(ABC):
    """Interface para o repositório de professores."""

    @abstractmethod
    def create_teacher(self, teacher_data: Teacher) -> None:
        """Cria um novo professor no banco de dados."""
        pass

    @abstractmethod
    def get_teacher_by_email(self, email: str) -> TeacherTable | None:
        """Retorna um professor pelo email."""
        pass
    
    @abstractmethod
    def get_all_teachers(self) -> list[TeacherTable]:
        """Retorna todos os professores cadastrados."""
        pass
    
    @abstractmethod
    def get_teacher_by_id(self, teacher_id: int) -> TeacherTable | None:
        """Retorna um professor pelo ID."""
        pass
