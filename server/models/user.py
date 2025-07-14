# models/user.py

from flask_login import UserMixin
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.security import check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["croppulse"]
users_collection = db["users"]

class User(UserMixin):
    def __init__(self, id, username, is_admin):
        self.id = str(id)
        self.username = username
        self.is_admin = is_admin

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": ObjectId(user_id)})
        if user_data:
            return User(str(user_data["_id"]), user_data["email"], user_data.get("role") == "admin")
        return None

    @staticmethod
    def authenticate(username, password):
        user_data = users_collection.find_one({"email": username})
        if user_data and check_password_hash(user_data["password"], password):
            return User(str(user_data["_id"]), user_data["email"], user_data.get("role") == "admin")
        return None
