from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os

bp = Blueprint("disease", __name__, url_prefix="/disease")

UPLOAD_FOLDER = os.path.join("uploads", "disease_images")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FOLDER = os.path.join(BASE_DIR, "..", "models", "disease")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cache loaded models and class labels
loaded_models = {}
crop_labels = {
    "apple": ["Apple_scab", "Black_rot", "Cedar_apple_rust", "Healthy"],
    "cherry": ["Powdery_mildew", "Healthy"],
    "corn": ["Cercospora_leaf_spot", "Common_rust", "Northern_Leaf_Blight", "Healthy"],
    "grape": ["Black_rot", "Esca", "Leaf_blight", "Healthy"],
    "peach": ["Bacterial_spot", "Healthy"],
    "pepper": ["Bacterial_spot", "Healthy"],
    "potato": ["Early_blight", "Late_blight", "Healthy"],
    "strawberry": ["Leaf_scorch", "Healthy"],
    "tomato": [
        "Bacterial_spot", "Early_blight", "Late_blight", "Leaf_Mold", "Septoria_leaf_spot",
        "Spider_mites", "Target_Spot", "Yellow_Leaf_Curl_Virus", "Mosaic_virus", "Healthy"
    ],
}

def get_model(crop):
    crop = crop.lower()
    if crop in loaded_models:
        print(f"Using cached model for crop: {crop}")
        return loaded_models[crop]

    model_path = os.path.join(MODEL_FOLDER, f"{crop}_model.h5")
    print(f"Looking for model at: {model_path}")
    if not os.path.exists(model_path):
        print(f"Model not found for crop: {crop}")
        raise FileNotFoundError(f"Model for '{crop}_model' not found at: {model_path}")

    model = load_model(model_path, compile=False)
    print(f"Model loaded successfully for crop: {crop}")
    loaded_models[crop] = model
    return model


@bp.route("/detect", methods=["POST"])
@jwt_required()
def predict_disease():
    if 'image' not in request.files or 'category' not in request.form:
        print("Bad request: missing image or category")
        return jsonify({"error": "Both 'image' and 'category' are required"}), 400

    img_file = request.files['image']
    crop = request.form['category'].lower().strip()

    if img_file.filename == "" or not crop:
        print("Bad request: image filename or category is empty")
        return jsonify({"error": "Missing image or category"}), 400

    filename = secure_filename(img_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img_file.save(filepath)
    print(f"Image saved at: {filepath}")

    try:
        model = get_model(crop)
        labels = crop_labels.get(crop, [])

        print("Preprocessing image...")
        img = image.load_img(filepath, target_size=(256, 256))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        print("Making prediction...")
        prediction = model.predict(img_array)
        predicted_index = int(np.argmax(prediction[0]))
        confidence = float(np.max(prediction[0]))

        print(f"Prediction complete. Index: {predicted_index}, Confidence: {confidence:.2f}")

        result = {
            "predicted_index": predicted_index,
            "confidence": round(confidence * 100, 2),
            "predicted_label": labels[predicted_index] if predicted_index < len(labels) else f"Class {predicted_index}"
        }

        return jsonify(result)

    except FileNotFoundError as e:
        print(f"File not found error: {str(e)}")
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print(f"Unexpected error during prediction: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted uploaded file: {filepath}")
