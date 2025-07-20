from pydantic import BaseModel

class ExamValidBody(BaseModel):
    subject: str
    teacher_id: int