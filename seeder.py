from pymongo import MongoClient

# Connect to MongoDB (replace with your connection string if using MongoDB Atlas)
client = MongoClient("mongodb+srv://ansarinadeem0625:nadeeMango@cluster0.csrjh.mongodb.net/")
db = client["student_management"]  # Database name
students_collection = db["students"]  # Collection name

# Sample student data with 'student_class' key added
students_data = [
    {
        "id": "1",
        "name": "Deepak Sharma",
        "age": 20,
        "email": "deepak.sharma@example.com",
        "enrollment_date": "2022-09-01",
        "courses": ["Mathematics", "Computer Science"],
        "GPA": 3.8,
        "status": "active",
        "student_class": "Sophomore"
    },
    {
        "id": "2",
        "name": "Ravi Patel",
        "age": 22,
        "email": "ravi.patel@example.com",
        "enrollment_date": "2021-09-01",
        "courses": ["Biology", "Chemistry"],
        "GPA": 3.5,
        "status": "active",
        "student_class": "Junior"
    },
    {
        "id": "3",
        "name": "Aarav Verma",
        "age": 19,
        "email": "aarav.verma@example.com",
        "enrollment_date": "2023-09-01",
        "courses": ["History", "Political Science"],
        "GPA": 3.9,
        "status": "active",
        "student_class": "Freshman"
    },
    {
        "id": "4",
        "name": "Sanya Iyer",
        "age": 21,
        "email": "sanya.iyer@example.com",
        "enrollment_date": "2020-09-01",
        "courses": ["Physics", "Astronomy"],
        "GPA": 3.2,
        "status": "graduated",
        "student_class": "Senior"
    },
    {
        "id": "5",
        "name": "Kabir Singh",
        "age": 23,
        "email": "kabir.singh@example.com",
        "enrollment_date": "2019-09-01",
        "courses": ["Economics", "Philosophy"],
        "GPA": 3.1,
        "status": "inactive",
        "student_class": "Alumnus"
    }
]


# Insert data into the collection
students_collection.insert_many(students_data)
print("Data seeded successfully!")

# Close the connection
client.close()
