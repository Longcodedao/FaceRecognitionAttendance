from flask import Flask
from pymongo import MongoClient

# MongoDB configuration
client = MongoClient('mongodb://localhost:27017/')
db = client['students_database']
students_collection = db['students']