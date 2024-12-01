from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

# Initialize FastAPI
app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://ansarinadeem0625:nadeeMango@cluster0.csrjh.mongodb.net/")
db = client.student_management

# Pydantic model for Student
class Student(BaseModel):
    name: str
    age: int
    student_class: str

# Create a new student
@app.post("/students")
async def create_student(student: Student):
    result = await db["students"].insert_one(student.dict())
    return {"id": str(result.inserted_id), **student.dict()}

# Get all students
@app.get("/students")
async def get_students():
    students = await db["students"].find().to_list(100)
    return students

# Get a student by ID
@app.get("/students/{id}")
async def get_student(id: str):
    student = await db["students"].find_one({"_id": id})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
@app.get("/")
async def root():
    return {"message": "Hello World"}

