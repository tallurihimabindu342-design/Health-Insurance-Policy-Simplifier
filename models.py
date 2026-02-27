from pydantic import BaseModel
from typing import List

class QuestionRequest(BaseModel):
    question: str

class Citation(BaseModel):
    page: str
    content: str

class AnswerResponse(BaseModel):
    answer: str
    citations: List[Citation]