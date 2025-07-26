from abc import ABC, abstractmethod

class IGetAnswerById(ABC):
    """Class Interface para o serviço de obtenção de resposta por ID."""

    @abstractmethod
    def execute(self, answer_id: str) -> dict:
        """
        Retrieves an answer by its ID.

        :param answer_id: The unique identifier of the answer.
        :return: A dictionary containing the answer details.
        """
        pass
