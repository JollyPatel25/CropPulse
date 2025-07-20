from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pymongo import MongoClient
from bson import ObjectId
import os
from dotenv import load_dotenv

# Load MongoDB and connect
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["croppulse"]
users_collection = db["users"]

bp = Blueprint('admin', __name__, url_prefix='/admin')

@bp.route('/crops/refresh-data', methods=['POST'])
@jwt_required()
def refresh_data():
    user_id = get_jwt_identity()  # 👈 Get user ID from JWT
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user or user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    try:
        from utils.refresh_crop_data import refresh_crop_data
        print("Refreshing dataset...", flush=True)
        refresh_crop_data()
        return jsonify({"message": "Dataset refreshed"}), 200
    except Exception as e:
        print("Error:", e)
        return jsonify({"error": str(e)}), 500

# routes/admin.py
@bp.route('/crops/train-model', methods=['POST'])
@jwt_required()
def train_model():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user or user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    try:
        from utils.train_crop_recommend_model import train_crop_model
        train_crop_model()
        return jsonify({"message": "Model trained successfully."}), 200
    except Exception as e:
        print(" Error training model:", e)
        return jsonify({"error": str(e)}), 500

@bp.route('/crops/clean-data', methods=['POST'])
@jwt_required()
def clean_data():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user or user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    try:
        from utils.clean_crop_data import clean_crop_data
        clean_crop_data()
        return jsonify({"message": "Data cleaned successfully."}), 200
    except Exception as e:
        print(" Error cleaning data:", e)
        return jsonify({"error": str(e)}), 500

# Fertilizer routes
@bp.route('/fertilizer/refresh-data', methods=['POST'])
@jwt_required()
def refresh_fertilizer():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user or user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    try:
        from utils.refresh_fertilizer_data import refresh_fertilizer_data
        refresh_fertilizer_data()
        return jsonify({"message": "Fertilizer dataset refreshed."}), 200
    except Exception as e:
        print("Error refreshing fertilizer data:", e)
        return jsonify({"error": str(e)}), 500

@bp.route('/fertilizer/clean-data', methods=['POST'])
@jwt_required()
def clean_fertilizer():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user or user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    try:
        from utils.clean_fertilizer_data import clean_fertilizer_data
        clean_fertilizer_data()
        return jsonify({"message": "Fertilizer data cleaned successfully."}), 200
    except Exception as e:
        print("Error cleaning fertilizer data:", e)
        return jsonify({"error": str(e)}), 500

@bp.route('/fertilizer/train-model', methods=['POST'])
@jwt_required()
def train_fertilizer():
    user_id = get_jwt_identity()
    user = users_collection.find_one({"_id": ObjectId(user_id)})

    if not user or user.get("role") != "admin":
        return jsonify({"error": "Forbidden"}), 403

    try:
        from utils.train_fertilizer_model import train_fertilizer_model
        train_fertilizer_model()
        return jsonify({"message": "Fertilizer model trained successfully."}), 200
    except Exception as e:
        print("Error training fertilizer model:", e)
        return jsonify({"error": str(e)}), 500
