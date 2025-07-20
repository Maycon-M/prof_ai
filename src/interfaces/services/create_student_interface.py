from abc import ABC, abstractmethod

class ICreateStudent(ABC):
    """Classe interface para criação de estudantes."""
    
    @abstractmethod
    async def execute(self, student_dto: dict) -> dict:
        """Create a new student with the provided data.

        Args:
            student_dto (dict): A dictionary containing student information.

        Returns:
            dict: A dictionary containing the created student's information.
        """
        pass
