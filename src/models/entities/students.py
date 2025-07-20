from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP
from src.models.base import Base

class StudentTable(Base):
    """Classe que define a tabela de estudantes no banco de dados."""
    
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(VARCHAR(255), nullable=False)
    registration_number = Column(VARCHAR(50), unique=True, nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    
    def __repr__(self):
        return f"<StudentTable(id={self.id}, name={self.name}, registration_number={self.registration_number}, created_at={self.created_at})>"