# INTERFACES
from src.interfaces.models.teachers_repository_interface import ITeachersRepository
from src.interfaces.models.db_connection_interface import IDataBaseConnectionHandler

# TABELA
from src.models.entities.teachers import TeacherTable

# SCHEMA
from src.schemas.teachers import Teacher

class TeachersRepository (ITeachersRepository):
    """Repositório para gerenciar operações relacionadas à tabela de professores."""

    def __init__(self, db_conn_handler: IDataBaseConnectionHandler) -> None:
        self.__db_conn_handler = db_conn_handler

    def create_teacher(self, teacher_data: Teacher) -> None:
        """Cria um novo professor no banco de dados."""
        with self.__db_conn_handler as database:
            try:
                data_object = TeacherTable(
                    name=teacher_data.name,
                    email=teacher_data.email,
                    created_at=teacher_data.created_at
                )
                database.session.add(data_object)
                database.session.commit()

            except Exception as e:
                database.session.rollback()
                raise e

    # TODO: Implementar serviços de busca por nome e email
    def get_teacher_by_email(self, email: str) -> TeacherTable | None:
        """Retorna um professor pelo email."""
        with self.__db_conn_handler as database:
            try:
                teacher = database.session.query(TeacherTable).filter_by(email=email).first()
                return teacher

            except Exception as e:
                raise e
    
    def get_all_teachers(self) -> list[TeacherTable]:
        """Retorna todos os professores cadastrados."""
        with self.__db_conn_handler as database:
            try:
                teachers = database.session.query(TeacherTable).all()
                return teachers

            except Exception as e:
                raise e
    
    # TODO: Implementar serviço de busca por ID
    def get_teacher_by_id(self, teacher_id: int) -> TeacherTable | None:
        """Retorna um professor pelo ID."""
        with self.__db_conn_handler as database:
            try:
                teacher = database.session.query(TeacherTable).filter_by(id=teacher_id).first()
                return teacher

            except Exception as e:
                raise e
