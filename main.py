from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from bson import ObjectId,json_util
import json


# Initialize FastAPI
app = FastAPI()

# MongoDB connection
client = AsyncIOMotorClient("mongodb+srv://ansarinadeem0625:nadeeMango@cluster0.csrjh.mongodb.net/")
db = client.student_management

# Pydantic model for Student
class Student(BaseModel):
     name: str
     age: int
     Student_class: str

    

@app.get("/")
async def root():
    return {"message": "Students management system"}

# Create a new student
@app.post("/students")
async def create_student(student: Student):
    result = await db["students"].insert_one(student.dict())
    return {"id": str(result.inserted_id), **student.dict()}

# Get all students
@app.get("/students")
async def get_students():
    students = await db["students"].find().to_list(100)
    return transform_student(json.loads(json_util.dumps(students)) )

# Get a student by ID
@app.get("/students/{id}")
async def get_student(id: str):
    student = await db["students"].find_one({"_id":ObjectId(id)})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return transform_student(json.loads(json_util.dumps(student)) )

def transform_student(student):
    student["id"] = student.get("_id")
    return student





