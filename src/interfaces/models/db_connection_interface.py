from abc import ABC, abstractmethod

class IDataBaseConnectionHandler(ABC):
    """
    Classe interface para conexão com banco de dados.
    """
    
    @abstractmethod
    def connect_to_db (self):
        pass
    
    @abstractmethod
    def get_engine (self):
        pass
    
    @abstractmethod
    def __enter__ (self):
        pass
    
    @abstractmethod
    def __exit__ (self, exc_type, exc_val, exc_tb):
        pass
