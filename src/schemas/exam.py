from datetime import datetime
from pydantic import BaseModel


class Exam (BaseModel):
    
    """Modelo de dados para uma prova.
    
    Attributes:
        subject (str): Nome da disciplina da prova.
        teacher_id (int): ID do professor responsável pela prova.
        time_stamp (datetime): Data e hora de criação da prova.
        correction_status (str): Status da correção da prova.    
    """
    
    subject: str
    teacher_id: int
    time_stamp: datetime
    correction_status: str
