# INTERFACES
from src.interfaces.models.students_repository_interface import IStudentsRepository
from src.interfaces.models.db_connection_interface import IDataBaseConnectionHandler

# TABELA
from src.models.entities.students import StudentTable

# SCHEMA
from src.schemas.student import Student

class StudentsRepository (IStudentsRepository):
    """Repositório para gerenciar operações relacionadas à tabela de estudantes."""

    def __init__(self, db_conn_handler: IDataBaseConnectionHandler) -> None:
        self.__db_conn_handler = db_conn_handler

    def create_student(self, student_data: Student) -> None:
        """Cria um novo estudante no banco de dados."""
        with self.__db_conn_handler as database:
            try:
                data_object = StudentTable(
                    full_name=student_data.full_name,
                    registration_number=student_data.registration_number,
                    created_at=student_data.created_at
                )
                database.session.add(data_object)
                database.session.commit()

            except Exception as e:
                database.session.rollback()
                raise e

    def get_student_by_registration_number(self, registration_number: str) -> StudentTable | None:
        """Retorna um estudante pelo número de matrícula."""
        with self.__db_conn_handler as database:
            try:
                student = database.session.query(StudentTable).filter_by(registration_number=registration_number).first()
                return student

            except Exception as e:
                raise e
            
    def get_all_students(self) -> list[StudentTable]:
        """Retorna todos os estudantes cadastrados."""
        with self.__db_conn_handler as database:
            try:
                students = database.session.query(StudentTable).all()
                return students

            except Exception as e:
                raise e
    
    def get_student_by_id(self, student_id: int) -> StudentTable | None:
        """Retorna um estudante pelo ID."""
        with self.__db_conn_handler as database:
            try:
                student = database.session.query(StudentTable).filter_by(id=student_id).first()
                return student

            except Exception as e:
                raise e