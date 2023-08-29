from flask import Flask
from pymongo import MongoClient, ASCENDING

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['students_database']
students_collection = db['students']
students_attendance = db['attendance']

students_collection.create_index([("student_id", ASCENDING)], unique = True)