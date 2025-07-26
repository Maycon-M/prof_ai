# INTERFACES
from src.interfaces.models.answers_repository_interface import IAnswersRepository
from src.interfaces.models.db_connection_interface import IDataBaseConnectionHandler

# TABELA
from src.models.entities.answers import AnswersTable

class AnswersRepository (IAnswersRepository):
    """Repositório para gerenciar operações relacionadas à tabela de respostas.
    
    Arguments:
        db_connection (IDataBaseConnectionHandler): Interface para manipulação de conexão com o banco de dados.
    """    
    def __init__(self, db_connection: IDataBaseConnectionHandler):
        self._db_connection = db_connection

    async def get_all_answers(self) -> list[AnswersTable]:
        """Retorna todas as respostas cadastradas.
        
        Returns:
            list[AnswersTable]: Lista de objetos AnswersTable representando as respostas.
            
        Raises:
            Exception: Se ocorrer um erro ao consultar o banco de dados.
        """
        
        with self._db_connection as database:
            try:
                answers = database.session.query(AnswersTable).all()
                return answers
            except Exception as e:
                raise e
    
    async def insert_answer(self, answer_data: dict) -> None:
        """Insere uma nova resposta no banco de dados.
        
        Args:
            answer_data (dict): Dados da resposta a serem inseridos, incluindo question_id, student_id, answer_text, created_at e correnction_status.
        
        Raises:
            Exception: Se ocorrer um erro ao inserir a resposta no banco de dados.        
        """
        
        with self._db_connection as database:
            try:
                answer = AnswersTable(
                    question_id=answer_data["question_id"],
                    student_id=answer_data["student_id"],
                    answer_text=answer_data["answer_text"],
                    created_at=answer_data["created_at"],
                    correction_status=answer_data["correction_status"],
                )
                database.session.add(answer)
                database.session.commit()
            except Exception as e:
                database.session.rollback()
                raise e
    
    async def get_answer_by_id(self, answer_id: int) -> AnswersTable | None:
        """Retorna uma resposta pelo ID.
        
        Args:
            answer_id (int): ID da resposta a ser recuperada.
            
        Returns:
            AnswersTable | None: Objeto AnswersTable representando a resposta, ou None se não encontrada.
            
        Raises:
            Exception: Se ocorrer um erro ao consultar o banco de dados.        
        """
        
        with self._db_connection as database:
            try:
                answer = database.session.query(AnswersTable).filter_by(id=answer_id).first()
                return answer
            except Exception as e:
                raise e
    
    async def get_answers_by_question_id(self, question_id: int) -> list[AnswersTable]:
        """Retorna todas as respostas associadas a uma pergunta específica.
        
        Args:
            question_id (int): ID da pergunta cujas respostas serão recuperadas.
        
        Returns:
            list[AnswersTable]: Lista de objetos AnswersTable representando as respostas associadas à pergunta.
            
        Raises:
            Exception: Se ocorrer um erro ao consultar o banco de dados.        
        """
        
        with self._db_connection as database:
            try:
                answers = database.session.query(AnswersTable).filter_by(question_id=question_id).all()
                return answers
            except Exception as e:
                raise e

    async def get_answers_by_student_id(self, student_id: int) -> list[AnswersTable]:
        """Retorna todas as respostas associadas a um estudante específico.
        
        Args:
            student_id (int): ID do estudante cujas respostas serão recuperadas.
            
        Returns:
            list[AnswersTable]: Lista de objetos AnswersTable representando as respostas associadas ao estudante.
            
        Raises:
            Exception: Se ocorrer um erro ao consultar o banco de dados.
        """
        
        with self._db_connection as database:
            try:
                answers = database.session.query(AnswersTable).filter_by(student_id=student_id).all()
                return answers
            except Exception as e:
                raise e

    async def update_score (self, answer_id: int, score: float, status: str) -> None:
        """Atualiza a pontuação de uma resposta.
        
        Args:
            answer_id (int): ID da resposta a ser atualizada.
            score (float): Nova pontuação a ser atribuída à resposta.
        
        Raises:
            Exception: Se ocorrer um erro ao atualizar a pontuação no banco de dados.
        """
        
        with self._db_connection as database:
            try:
                answer = database.session.query(AnswersTable).filter_by(id=answer_id).first()
                if answer:
                    answer.score = score
                    answer.correction_status = status
                    database.session.commit()
                else:
                    raise ValueError(f"Answer with ID {answer_id} not found.")
            except Exception as e:
                database.session.rollback()
                raise e
