from pydantic import BaseModel
from typing import List

class Answer(BaseModel):
    question_id: int
    student_id: int
    answer_text: str
    
class AnswersValidBody(BaseModel):
    answers: List[Answer]
