from fastapi import APIRouter
from serializer import student_serializer
from fastapi.exceptions import HTTPException

Students = student_serializer.StudentBaseModel

router = APIRouter()

# Get all students
@router.get("/students")
async def get_students():
    students = list(await db["students"].find().to_list(100))
    return Students.StudentListModel(students=students).model_dump()

# Get a student by ID
@router.get("/students/{id}")
async def get_student(id: str):
    student = await db["students"].find_one({"_id": ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Create a new student
@router.post("/students")
async def create_student(data: dict):
    student =  Students.StudentBaseModel(**data)
    result = await db["students"].insert_one(student)
    return
