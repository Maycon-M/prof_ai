from pydantic import BaseModel
from typing import List

class QuestionAttributes(BaseModel):
    question: str
    number: int
    
class ValidQuestionsBody(BaseModel):
    questions: List[QuestionAttributes]
    
