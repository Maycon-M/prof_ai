# INTERFACES
from src.interfaces.models.db_connection_interface import IDataBaseConnectionHandler
from src.interfaces.models.exams_repository_interface import IExamsRepository

# TABELA
from src.models.entities.exams import ExamsTable

# SCHEMAS
from src.schemas.exam import Exam

class ExamsRepository (IExamsRepository):
    """Repositorio para manipular as operações relacionadas as provas.
    
    Attributes:
        __db_conn_handler (IDataBaseConnectionHandler): Interface para manipulação de conexões com o banco de dados.
        
    Methods:
        create_exam(exam_data: dict) -> None: Cria uma nova prova no banco de dados.
    """

    def __init__ (self, db_conn_handler: IDataBaseConnectionHandler) -> None:
        self.__db_conn_handler = db_conn_handler

    def create_exam(self, exam_data: Exam) -> None:
        """Cria uma nova prova no banco de dados."""
        with self.__db_conn_handler as database:
            try:
                data_object = ExamsTable(
                    subject_name=exam_data.subject,
                    created_at=exam_data.time_stamp,
                    correction_status=exam_data.correction_status,
                    teacher_id=exam_data.teacher_id
                )
                database.session.add(data_object)
                database.session.commit()

            except Exception as e:
                database.session.rollback()
                raise e
