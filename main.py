from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from config.database import settings
from bson import ObjectId

# Initialize FastAPI
app = FastAPI()
client = AsyncIOMotorClient(settings.DB_URL)
db = client.student_management

@app.get("/")
async def root():
    return {"message": "Students management system API"}

@app.get("/students")
async def fetch_all_students():
    return await db["students"].find({}, {"_id": 0}).to_list();

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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('main:app', host=settings.HOST, port=settings.PORT, reload=True)
