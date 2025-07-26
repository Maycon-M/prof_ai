from pydantic import BaseModel, EmailStr

class TeacherValidationBody(BaseModel):
    name: str
    email: EmailStr
