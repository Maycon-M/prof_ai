from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# INTERFACES
from src.interfaces.models.db_connection_interface import IDataBaseConnectionHandler

from src.configs.postegres_string_config import PG_CONNECTION_STRING

class PostgresConnectionHandler(IDataBaseConnectionHandler):
    """
    Classe que implementa a conexão com o banco de dados PostgreSQL.
    """
    
    def __init__(self) -> None:
        self.__connection_string = PG_CONNECTION_STRING
        self.__engine = None
        self.session = None
        
    def connect_to_db (self):
        self.__engine = create_engine (self.__connection_string)
    
    def get_engine (self):
        if self.__engine is None:
            self.connect_to_db()
        return self.__engine
    
    def __enter__ (self):
        session_maker = sessionmaker()
        self.session = session_maker(bind=self.__engine)
        return self

    def __exit__ (self, exc_type, exc_val, exc_tb):
        self.session.close()

pg_connection_handler = PostgresConnectionHandler()