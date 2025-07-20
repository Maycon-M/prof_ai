from pydantic import BaseModel
from datetime import datetime

class Student(BaseModel):
    """Modelo de dados para um estudante.
    
    Attributes:
        full_name (str): Nome completo do estudante.
        registration_number (str): Número de matrícula do estudante.
        created_at (datetime): Data e hora de criação do registro do estudante.
    """
    
    full_name: str
    registration_number: str
    created_at: datetime
