from pydantic import BaseModel

class StudentValidationBody(BaseModel):
    full_name: str
    registration_number: str
