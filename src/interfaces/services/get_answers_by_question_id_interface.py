from abc import ABC, abstractmethod

class IGetAnswersByQuestionId(ABC):
    """Interface para obter respostas associadas a um question_id específico."""
    
    @abstractmethod
    def execute(self, question_id: int) -> dict:
        """Obtém todas as respostas associadas a um question_id específico.
        
        Args:
            question_id (int): ID da questão para a qual as respostas serão buscadas.
        
        Returns:
            dict: Dicionário contendo a lista de respostas associadas ao question_id.
        
        Raises:
            HttpNotFoundError: Se não forem encontradas respostas para o question_id fornecido.
            HttpInternalServerError: Se ocorrer um erro ao acessar o repositório de respostas.
        """
        pass
