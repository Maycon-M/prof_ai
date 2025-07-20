from abc import ABC, abstractmethod

# TABELA
from src.models.entities.answers import AnswersTable

class IAnswersRepository (ABC):
    
    """Interface para o repositório de respostas."""

    @abstractmethod
    async def get_all_answers(self) -> list[AnswersTable]:
        """Retorna todas as respostas cadastradas.
        
        Returns:
            list[AnswersTable]: Lista de objetos AnswersTable representando as respostas.
        """
        pass

    @abstractmethod
    async def insert_answer(self, answer_data: dict) -> None:
        """Insere uma nova resposta no banco de dados.
        
        Args:
            answer_data (dict): Dados da resposta a serem inseridos, incluindo question_id, student_id, answer_text, created_at e correnction_status. 
        """
        pass
    
    @abstractmethod
    async def get_answer_by_id(self, answer_id: int) -> AnswersTable | None:
        """Retorna uma resposta pelo ID.
        
        Args:
            answer_id (int): ID da resposta a ser recuperada.
            
        Returns:
            AnswersTable | None: Objeto AnswersTable representando a resposta, ou None se não encontrada.        
        """
        pass
    
    @abstractmethod
    async def get_answers_by_question_id(self, question_id: int) -> list[AnswersTable]:
        """Retorna todas as respostas associadas a uma pergunta específica.
        
        Args:
            question_id (int): ID da pergunta cujas respostas serão recuperadas.
        
        Returns:
            list[AnswersTable]: Lista de objetos AnswersTable representando as respostas associadas à pergunta. 
        """
        pass

    @abstractmethod
    async def get_answers_by_student_id(self, student_id: int) -> list[AnswersTable]:
        """Retorna todas as respostas associadas a um estudante específico.
        
        Args:
            student_id (int): ID do estudante cujas respostas serão recuperadas.
            
        Returns:
            list[AnswersTable]: Lista de objetos AnswersTable representando as respostas associadas ao estudante.
        """
        pass
