from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from routes import auth, admin, recommend, disease, fertilizer
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = "fallback_secret_key"
app.config["JWT_SECRET_KEY"] = "fallback_secret_key"
CORS(app, supports_credentials=True, origins=["http://localhost:3000"])

# JWT setup
jwt = JWTManager(app)

# JWT error handlers
@jwt.invalid_token_loader
def invalid_token_callback(reason):
    return jsonify({"message": "Invalid token"}), 401

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return jsonify({"message": "Token expired"}), 401

# Register blueprints
app.register_blueprint(auth.bp)
app.register_blueprint(admin.bp)
app.register_blueprint(recommend.bp)
app.register_blueprint(disease.bp)
app.register_blueprint(fertilizer.bp)

# 📦 Absolute path for uploads and fallback image
UPLOAD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), 'uploads'))
DEFAULT_IMAGE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'assets', 'default-profile.jpg'))

@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.isfile(file_path):
        return send_from_directory(UPLOAD_FOLDER, filename)
    else:
        return send_from_directory(os.path.dirname(DEFAULT_IMAGE), os.path.basename(DEFAULT_IMAGE))

@app.route('/')
def home():
    return {"message": "Welcome to CropPulse API"}

if __name__ == '__main__':
    app.run(debug=True)
