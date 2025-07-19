from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP, ForeignKey
from src.models.base import Base

class ExamsTable(Base):
    """
    Classe que define a tabela de provas no banco de dados.
    """
    
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_name = Column(VARCHAR(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    correction_status = Column(VARCHAR(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id", ondelete="CASCADE"), nullable=False)
    
    def __repr__(self):
        return f"<ExamsTable(id={self.id}, subject_name={self.subject_name}, created_at={self.created_at}, correction_status={self.correction_status}, teacher_id={self.teacher_id})>"
