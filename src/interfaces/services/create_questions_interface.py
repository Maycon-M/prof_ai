from abc import ABC, abstractmethod

class ICreateQuestionsService(ABC):
    
    """Classe Interface para o serviço de criação de questões."""
    
    @abstractmethod
    async def execute(self, questions_dto: dict, exam_id: int) -> dict:
        """Cria as novas questões recebidas no banco de dados.
        
        Args:
            questions_dto (dict): Dicionário contendo as questões a serem criadas.
            exam_id (int): ID da prova associada às questões.
            
        Returns:
            dict: Dicionário com o status da operação e mensagem de sucesso.
        """
        pass
