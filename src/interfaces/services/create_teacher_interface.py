from abc import ABC, abstractmethod

class ICreateTeacher(ABC):
    """Interface para a criação de professores."""

    @abstractmethod
    async def execute(self, teacher_dto: dict) -> dict:
        """Cria um novo professor com os dados fornecidos.
        
        Args:
            teacher_dto (dict): Um dicionário contendo as informações do professor.
            
        Returns:
            dict: Um dicionário contendo as informações do professor criado.
        
        Raises:
            HttpBadRequest: Se os dados do professor forem inválidos.
            HttpInternalServerError: Se ocorrer um erro ao inserir o professor no repositório.
        """
        pass
