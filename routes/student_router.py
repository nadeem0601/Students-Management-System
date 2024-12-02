from fastapi import APIRouter
import repository.students
from serializer import student_serializer
from fastapi.exceptions import HTTPException
from repository.students import StudentRepository


Students = student_serializer.StudentBaseModel
StudentListModel = student_serializer.StudentListModel

router = APIRouter()

# Get all students
@router.get("/students")
async def get_students():
    students = StudentRepository.fetch_all_students()
    return students

# Get a student by ID
@router.get("/students/{id}")
async def get_student(id: str):
    student = StudentRepository.fetch_student_by_id(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

# Create a new student
@router.post("/students")
async def create_student(data: dict):
    result = StudentRepository.add_student(data)
    return result

@router.patch("/students/{id}")
async def update_student(data: dict, id: str):
    is_updated = StudentRepository.update_student(id, data)
    return is_updated
