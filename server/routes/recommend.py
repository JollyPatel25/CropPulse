from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import numpy as np
import joblib
import os

bp = Blueprint('recommend', __name__, url_prefix='/recommend')

model = None

# 🔍 Determine absolute path to the model
base_dir = os.path.dirname(os.path.abspath(__file__))  # routes/
project_root = os.path.abspath(os.path.join(base_dir, ".."))
model_path = os.path.join(project_root, "models", "crop_model.pkl")

print(f" Looking for model at: {model_path}")

# 📦 Try to load the model
try:
    if os.path.exists(model_path):
        model = joblib.load(model_path)
        print(" Model loaded successfully.")
    else:
        print(f" Model file not found at {model_path}")
except Exception as e:
    print(f" Failed to load model: {e}")
    model = None

@bp.route('/crop', methods=['POST'])
@jwt_required()
def recommend_crop():
    if model is None:
        return jsonify({"error": "Model not loaded. Please train the model first."}), 500

    data = request.get_json()
    try:
        features = np.array([[ 
            float(data['N']), float(data['P']), float(data['K']),
            float(data['temperature']), float(data['humidity']),
            float(data['ph']), float(data['rainfall'])
        ]])

        # 🔍 Predict top 10 crops using probabilities
        probabilities = model.predict_proba(features)[0]
        class_labels = model.classes_

        top_indices = np.argsort(probabilities)[::-1][:5]
        top_predictions = [
            {"crop": class_labels[i], "confidence": round(probabilities[i] * 100, 2)}
            for i in top_indices
        ]

        return jsonify({"top_recommendations": top_predictions})

    except Exception as e:
        return jsonify({'error': f"Prediction error: {str(e)}"}), 400
