from abc import ABC, abstractmethod

class ICreateAnswers (ABC):
    
    @abstractmethod
    async def execute(self, answers_dto: dict) -> dict:
        """Cria as novas respostas recebidas no banco de dados.
        
        Args:
            answers_dto (dict): Dicionário contendo as respostas a serem criadas.
        
        Returns:
            dict: Dicionário com o status da operação e mensagem de sucesso.
        """
        pass
