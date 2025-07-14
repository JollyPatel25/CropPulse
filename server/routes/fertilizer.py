from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
import numpy as np
import joblib
import os
import time

bp = Blueprint('fertilizer', __name__, url_prefix='/fertilizer')

# 🔍 Define paths
base_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(base_dir, ".."))
model_dir = os.path.join(project_root, "models")

model_path = os.path.join(model_dir, "fertilizer_model.pkl")
fertilizer_enc_path = os.path.join(model_dir, "fertilizer_label_encoder.pkl")
soil_enc_path = os.path.join(model_dir, "soil_label_encoder.pkl")
crop_enc_path = os.path.join(model_dir, "crop_label_encoder.pkl")

# 🔄 Initial load
model = None
fertilizer_enc = None
soil_enc = None
crop_enc = None
last_model_load_time = 0
model_reload_interval = 60  # seconds

def reload_model_if_needed(force=False):
    global model, fertilizer_enc, soil_enc, crop_enc, last_model_load_time

    if force or time.time() - last_model_load_time > model_reload_interval or model is None:
        try:
            model = joblib.load(model_path)
            fertilizer_enc = joblib.load(fertilizer_enc_path)
            soil_enc = joblib.load(soil_enc_path)
            crop_enc = joblib.load(crop_enc_path)
            last_model_load_time = time.time()
            print("Fertilizer model and encoders reloaded.")
        except Exception as e:
            print(f"Failed to reload model or encoders: {e}")
            model = None
            fertilizer_enc = None
            soil_enc = None
            crop_enc = None
            raise e  # So /reload route can handle it too

@bp.route('', methods=['POST'])
@jwt_required()
def recommend_fertilizer():
    reload_model_if_needed()

    if not model or not fertilizer_enc or not soil_enc or not crop_enc:
        return jsonify({"error": "Model or encoders not loaded"}), 500

    try:
        data = request.get_json()

        # Convert categorical features to encoded form
        soil = soil_enc.transform([data["Soil Type"]])[0]
        crop = crop_enc.transform([data["Crop Type"]])[0]

        features = np.array([[ 
            float(data['Temperature']), float(data['Humidity']), float(data['Moisture']),
            float(data['Nitrogen']), float(data['Potassium']), float(data['Phosphorous']),
            soil, crop
        ]])

        probabilities = model.predict_proba(features)[0]
        class_labels = model.classes_

        top_indices = np.argsort(probabilities)[::-1][:3]
        top_predictions = [
            {
                "fertilizer": fertilizer_enc.inverse_transform([class_labels[i]])[0],
                "confidence": round(probabilities[i] * 100, 2)
            }
            for i in top_indices
        ]

        return jsonify({"top_recommendations": top_predictions})

    except Exception as e:
        return jsonify({'error': f"Prediction error: {str(e)}"}), 400

# 🔄 Admin-triggered reload endpoint
@bp.route('/reload', methods=['POST'])
@jwt_required()
def reload_model_now():
    try:
        reload_model_if_needed(force=True)
        return jsonify({"message": "Fertilizer model and encoders reloaded."}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
