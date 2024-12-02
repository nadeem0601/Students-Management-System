from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from config.database import settings
from routes.student_router import router as student_router

# Initialize FastAPI
app = FastAPI()
app.include_router(student_router)

# MongoDB connection
client = AsyncIOMotorClient(settings.DB_URL)
db = client.student_management

@app.get("/")
async def root():
    return {"message": "Students management system API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
