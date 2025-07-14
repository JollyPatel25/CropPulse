from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from werkzeug.utils import secure_filename
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os

bp = Blueprint("disease", __name__, url_prefix="/disease")

UPLOAD_FOLDER = os.path.join("uploads", "disease_images")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_FOLDER = os.path.join(BASE_DIR, "..", "models", "disease", "pbtype")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 🔖 Unified label list for the PB model
pb_labels = [
    "Tomato Healthy", "Tomato Septoria Leaf Spot", "Tomato Bacterial Spot", "Tomato Blight",
    "Cabbage Healthy", "Tomato Spider Mite", "Tomato Leaf Mold", "Tomato_Yellow Leaf Curl Virus",
    "Soy_Frogeye_Leaf_Spot", "Soy_Downy_Mildew", "Maize_Ravi_Corn_Rust", "Maize_Healthy",
    "Maize_Grey_Leaf_Spot", "Maize_Lethal_Necrosis", "Soy_Healthy", "Cabbage Black Rot"
]

# 🔄 Cache the model
loaded_model = None


def load_pb_model():
    global loaded_model
    if loaded_model is None:
        print(f"Loading .pb model from: {MODEL_FOLDER}")
        loaded_model = tf.keras.models.load_model(MODEL_FOLDER)
        print("Model loaded successfully.")
    return loaded_model


@bp.route("/detect", methods=["POST"])
@jwt_required()
def detect_disease():
    if 'image' not in request.files:
        print("Missing image file.")
        return jsonify({"error": "Image file is required"}), 400

    img_file = request.files['image']
    if img_file.filename == "":
        print("Empty image filename.")
        return jsonify({"error": "Image file is empty"}), 400

    filename = secure_filename(img_file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    img_file.save(filepath)
    print(f"Image saved at: {filepath}")

    try:
        model = load_pb_model()

        print("Preprocessing image...")
        img = image.load_img(filepath, target_size=(300, 300))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        print("Making prediction...")
        predictions = model.predict(img_array)

        # Handle (None, 10, 10) output shape
        flat = predictions.reshape(-1)
        predicted_index = int(np.argmax(flat))
        confidence = float(np.max(flat))

        print(f"Prediction complete. Index: {predicted_index}, Confidence: {confidence:.2f}")

        result = {
            "predicted_index": predicted_index,
            "confidence": round(confidence * 100, 2),
            "predicted_label": pb_labels[predicted_index] if predicted_index < len(pb_labels) else f"Class {predicted_index}"
        }

        return jsonify(result)

    except Exception as e:
        print(f"Prediction failed: {str(e)}")
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"Deleted uploaded file: {filepath}")
