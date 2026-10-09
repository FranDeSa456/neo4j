from pydantic import BaseModel


class StudentIn(BaseModel):
    name: str
    age: int

class CourseIn(BaseModel):
    name: str
    hours: int
