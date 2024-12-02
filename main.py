from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from config.database import settings
from bson import ObjectId
from typing import Optional

# Initialize FastAPI
app = FastAPI()
client = AsyncIOMotorClient(settings.DB_URL)
db = client.student_management

@app.get("/")
async def root():
    return {"message": "Students management system API"}

@app.get("/students")
async def fetch_all_students():
    return await db["students"].find({}, {"_id": 0}).to_list()

@app.post("/students")
async def create_student(student: dict):
    student_id = await db["students"].insert_one(student)
    return {"_id": str(student_id.inserted_id)}

@app.get("/students/search")
async def search_student(name: Optional[str] = "", email: Optional[str] = "", course: Optional[str] = "", status: Optional[str] = "", student_class: Optional[str] = ""):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if email:
        query["email"] = {"$regex": email, "$options": "i"}
    if course:
        query["courses"] = {"$regex": course, "$options": "i"}
    if status:
        query["status"] = {"$regex": status, "$options": "i"}
    if student_class:
        query["student_class"] = {"$regex": student_class, "$options": "i"}  # Case-insensitive search by class
    print(query)
    result = await db["students"].find(query, {"_id": 0}).to_list()
    return result

@app.get("/students/{id}")
async def fetch_student_by_id(id: str):
    return await db["students"].find_one({"_id": ObjectId(id)}, {"_id": 0})

@app.delete("/students/{id}")
async def delete_student(id: str):
    result = await db["students"].delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0

@app.patch("/students/{id}")
async def update_student(id: str, data: dict):
    result = await db["students"].update_one({"_id": ObjectId(id)}, {"$set": data})
    return result.modified_count > 0

@app.post("/students/{student_id}/enroll")
async def enroll_student(student_id: str, course: str):
    student = await db["students"].find_one({"_id": ObjectId(student_id)}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if course in student.get("courses", []):
        raise HTTPException(status_code=400, detail=f"{course} already enrolled")
    await db["students"].update_one({"_id": ObjectId(student_id)}, {"$push": {"courses": course}})
    return {"msg": f"{course} enrolled successfully!"}

@app.get("/students/{id}/courses")
async def get_student_courses(id: str):
    return await db["students"].find_one({"_id": ObjectId(id)}, {"courses": 1, "_id": 0})

@app.delete("/students/{id}/courses")
async def remove_student_course(id: str, course: str):
    student = await db["students"].find_one({"_id": ObjectId(id)}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    if course not in student.get("courses", []):
        raise HTTPException(status_code=400, detail=f"{course} is not enrolled in this student")
    result = await db["students"].update_one({"_id": ObjectId(id)}, {"$pull": {"courses": course}})
    return {"msg": f"{course} removed successfully!", "student": result}

@app.post("/students/{id}/graduation-status")
async def update_graduation_status(id: str, status: str):
    student = await db["students"].find_one({"_id": ObjectId(id)}, {"_id": 0})
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await db["students"].update_one({"_id": ObjectId(id)}, {"$set": {"status": status}})
    return {"msg": f"Graduation status updated to {status}!"}

@app.get("/students/{id}/graduation-status")
async def get_graduation_status(id: str):
    return await db["students"].find_one({"_id": ObjectId(id)}, {"name": 1, "enrollment_date": 1, "status": 1, "_id": 0})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=True)