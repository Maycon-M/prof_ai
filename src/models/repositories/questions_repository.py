# INTERFACES
from src.interfaces.models.questions_repository_interface import IQuestionsRepository
from src.interfaces.models.db_connection_interface import IDataBaseConnectionHandler

# TABELA
from src.models.entities.questions import QuestionsTable

class QuestionsRepository(IQuestionsRepository):
    
    def __init__(self, db_conn_handler: IDataBaseConnectionHandler) -> None:
        self.__db_conn_handler = db_conn_handler
    
    def create_question(self, question_data: dict) -> None:
        """Cria uma nova questão no banco de dados."""
        with self.__db_conn_handler as database:
            try:
                data_object = QuestionsTable(
                    exam_id=question_data['exam_id'],
                    question_text=question_data['text'],
                    created_at=question_data['created_at'],
                    correction_status=question_data['correction_status'],
                    question_number=question_data['number']
                )
                database.session.add(data_object)
                database.session.commit()

            except Exception as e:
                database.session.rollback()
                raise e
