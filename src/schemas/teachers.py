from pydantic import BaseModel, EmailStr 
from datetime import datetime

class Teacher(BaseModel):
    """Modelo de dados para um professor.
    
    Attributes:
        name (str): Nome completo do professor.
        email (EmailStr): Email do professor.
        created_at (datetime): Data e hora de criação do registro do professor.
    """
    
    name: str
    email: EmailStr
    created_at: datetime
