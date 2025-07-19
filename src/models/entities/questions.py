from sqlalchemy import Column, Integer, VARCHAR, Text, TIMESTAMP, ForeignKey
from src.models.base import Base

class QuestionsTable(Base):
    """
    Classe que define a tabela de questões no banco de dados.
    """
    
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(Text, nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    correction_status = Column(VARCHAR(100), nullable=False)
    
    def __repr__(self):
        return f"<QuestionsTable(id={self.id}, question_text={self.question_text}, exam_id={self.exam_id}, created_at={self.created_at}, correction_status={self.correction_status})>"