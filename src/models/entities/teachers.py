from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP
from src.models.base import Base

class TeacherTable (Base):
    
    __tablename__ = "teachers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, nullable=False)
    
    def __repr__(self):
        return f"<TeacherTable(id={self.id}, name={self.name}, email={self.email})>"