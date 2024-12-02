from config import database
from typing import List, Optional

class StudentRepository:
    def __init__(self, client):
        self.client = client
        self.db = self.client[database.settings.DB_NAME]
        self.collection = self.db["student"]

    def fetch_all_students(self) -> List[dict]:
        return list(self.collection.find({}, {"_id": 0}))

    def fetch_student_by_id(self, student_id: str) -> Optional[dict]:
        return self.collection.find_one({"_id": student_id})

    def add_student(self, student_data: dict) -> str:
        result = self.collection.insert_one(student_data);
        return str(result.inserted_id)

    def update_student(self, student_id: str, update_data: dict) -> bool:
        result = self.collection.update_one({"_id": student_id}, {"$set": update_data})
        return result.modified_count > 0

    def delete_student(self, student_id: str) -> bool:
        result = self.collection.delete_one({"_id": student_id})
        return result.deleted_count > 0

    def close_connection(self):
        self.client.close()
