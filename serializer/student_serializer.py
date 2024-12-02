from pydantic import BaseModel, Field
from datetime import datetime
from typing import List
from datetime import datetime
from bson import ObjectId

class StudentBaseModel(BaseModel):
    id: str = Field(alias="_id")
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