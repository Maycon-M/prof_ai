from sqlalchemy import Column, Integer, VARCHAR, Text, TIMESTAMP, ForeignKey, Numeric
from src.models.base import Base

class AnswersTable(Base):
    """
    Classe que define a tabela de respostas no banco de dados.
    """
    
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    answer_text = Column(Text, nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False)
    score = Column(Numeric(5,2), nullable=True)
    correnction_status = Column(VARCHAR(100), nullable=False)
    
    
    def __repr__(self):
        return f"<AnswersTable(id={self.id}, answer_text={self.answer_text}, question_id={self.question_id}, created_at={self.created_at}, is_correct={self.is_correct})>"
