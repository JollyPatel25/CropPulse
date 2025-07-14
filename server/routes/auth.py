from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import shutil
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from bson import ObjectId
from datetime import timedelta
import re, os
from pymongo import MongoClient
from dotenv import load_dotenv

# Blueprint setup
bp = Blueprint('auth', __name__, url_prefix='/auth')

# Load MongoDB credentials from .env
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["croppulse"]
users_collection = db["users"]
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
UPLOAD_FOLDER = os.path.abspath(UPLOAD_FOLDER)
DEFAULT_IMAGE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'assets', 'default-profile.jpg'))
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# 🚀 Register Route
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    required_fields = ["email", "password", "confirm_password", "name", "birth_date",
                       "street", "city", "state", "pincode"]
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"message": "Passwords do not match"}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({"message": "Invalid email format"}), 400

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 409

    email = data["email"]
    username = email.split("@")[0]  
    profilepic_filename = f"{username}.jpg"

    new_user = {
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "name": data["name"],
        "birth_date": data["birth_date"],
        "address": {
            "street": data["street"],
            "city": data["city"],
            "state": data["state"],
            "pincode": data["pincode"]
        },
        "role": "user",
        "profile_image": profilepic_filename
    }

    result = users_collection.insert_one(new_user)
    access_token = create_access_token(identity=str(result.inserted_id), expires_delta=timedelta(days=1))
    
    return jsonify({
        "message": "Registration successful",
        "token": access_token
    }), 201


# 🔐 Login Route
@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = users_collection.find_one({"email": data.get("username")})
    
    if user and check_password_hash(user["password"], data.get("password")):
        access_token = create_access_token(identity=str(user["_id"]), expires_delta=timedelta(days=1))
        return jsonify({
            "message": "Login successful",
            "token": access_token,
            "user": {
                "id": str(user["_id"]),
                "username": user["email"],
                "is_admin": user.get("role") == "admin"
            }
        })

    return jsonify({"message": "Invalid credentials"}), 401


# ✅ Verify Token Route
@bp.route('/verify-token', methods=['GET'])
@jwt_required()
def verify_token():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"message": "User not found"}), 404

    user_data = {
        "id": str(user["_id"]),
        "email": user.get("email"),
        "username": user.get("email"),
        "name": user.get("name"),
        "birth_date": user.get("birth_date"),
        "profile_image": user.get("profile_image", ""),
        "address": {
            "street": user.get("address", {}).get("street", ""),
            "city": user.get("address", {}).get("city", ""),
            "state": user.get("address", {}).get("state", ""),
            "pincode": user.get("address", {}).get("pincode", "")
        },
        "is_admin": user.get("role") == "admin"
    }

    return jsonify({"user": user_data}), 200


# 👤 Get Profile Route
@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"message": "User not found"}), 404

    if user.get("profile_image"):
        image_path = os.path.join(UPLOAD_FOLDER, user["profile_image"])
        if not os.path.isfile(image_path):
            if os.path.isfile(DEFAULT_IMAGE):
                shutil.copy(DEFAULT_IMAGE, image_path)
            else:
                print("Default profile image missing in assets/")

    user["_id"] = str(user["_id"])
    return jsonify(user)


# ✏️ Update Profile Route
@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"message": "User not found"}), 404

    data = request.form.to_dict()
    address = {
        "street": data.get("street"),
        "city": data.get("city"),
        "state": data.get("state"),
        "pincode": data.get("pincode")
    }

    update_data = {
        "name": data.get("name"),
        "birth_date": data.get("birth_date"),
        "address": address
    }

    if 'profile_image' in request.files:
        file = request.files['profile_image']
        if file:
            filename = secure_filename(user['email'].split("@")[0] + ".jpg")
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            file.save(filepath)
            update_data["profile_image"] = filename
    else:
        filename = secure_filename(user['email'].split("@")[0] + ".jpg")
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        if not os.path.isfile(filepath) and os.path.isfile(DEFAULT_IMAGE):
            shutil.copy(DEFAULT_IMAGE, filepath)
            update_data["profile_image"] = filename

    users_collection.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
    updated_user["_id"] = str(updated_user["_id"])

    return jsonify(updated_user)


# 🔓 Logout Route
@bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({"message": "Logged out (client should delete token)"}), 200


# 🗑️ Delete Profile Image Route
@bp.route('/delete-image', methods=['DELETE'])
@jwt_required()
def delete_image():
    image_name = request.args.get("image")
    if not image_name:
        return jsonify({"message": "Image name not provided"}), 400

    image_path = os.path.join(UPLOAD_FOLDER, image_name)
    if os.path.exists(image_path):
        os.remove(image_path)

        user_id = get_jwt_identity()
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$unset": {"profile_image": ""}}
        )
        return jsonify({"message": "Image deleted", "profile_image": None}), 200

    return jsonify({"message": "Image not found"}), 404
    