from pydantic import BaseModel
from typing import List, Optional
 
class Question(BaseModel):
    question: str
    answer: str
    type: str
    question_slug: str
    reference_id: str
    hint: Optional[str] = None
    params: Optional[dict] = {}

class Section(BaseModel):
    marks_per_question: int
    type: str
    questions: List[Question]

class Params(BaseModel):
    board: str
    grade: int
    subject: str

class SamplePaper(BaseModel):
    title: str
    type: str
    time: int
    marks: int
    params: Params
    tags: List[str]
    chapters: List[str]
    sections: List[Section]

class SamplePaperUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    time: Optional[int] = None
    marks: Optional[int] = None
    params: Optional[Params] = None
    tags: Optional[List[str]] = None
    chapters: Optional[List[str]] = None
    sections: Optional[List[Section]] = None
