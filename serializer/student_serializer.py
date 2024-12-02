from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import List
from datetime import datetime
from bson import ObjectId

class StudentBaseModel(BaseModel):
    name: str
    age: int
    email: str
    enrollment_date: str
    courses: List[str]
    GPA: float
    status: str
    student_class: str

    class Config:
        populate_by_name = True
        json_encoders = {
            ObjectId: lambda v: str(v),
            datetime: lambda v: v.isoformat()
        }


class StudentListModel(BaseModel):
    students: List[StudentBaseModel]