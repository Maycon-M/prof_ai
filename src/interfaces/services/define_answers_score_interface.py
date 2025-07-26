from abc import ABC, abstractmethod

class IDefineAnswersScore(ABC):
    """Interface para definir a pontuação de respostas."""

    @abstractmethod
    async def execute(self, answer_id: int, score: float) -> None:
        """Define a pontuação de uma resposta.
        
        Args:
            answer_id (int): ID da resposta cuja pontuação será definida.
            score (float): Pontuação a ser atribuída à resposta.
        
        Raises:
            HttpNotFoundError: Se a resposta não for encontrada.
            HttpBadRequestError: Se a pontuação for inválida.
            HttpInternalServerError: Se ocorrer um erro ao atualizar a pontuação.
        """
        pass
