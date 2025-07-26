from abc import ABC, abstractmethod

class IGetAnswersByStudentId(ABC):
    """ Classe Interface para obter respostas por ID de aluno. """
    
    @abstractmethod
    async def execute(self, student_id: int) -> dict:
        """Obtém as respostas de um aluno específico pelo ID.
        
        Args:
            student_id (int): ID do aluno cujas respostas serão recuperadas.
        
        Returns:
            dict: Dicionário contendo as respostas do aluno ou uma mensagem de erro.
        """
        pass
