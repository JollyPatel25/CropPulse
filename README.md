# 🌿 CropPulse - Smart Crop Advisory System
CropPulse is an AI-powered smart crop advisory system that recommends the best crops, suitable fertilizers, and detects plant diseases using ML models. It provides a user-friendly interface for farmers and an admin dashboard for managing datasets and retraining models, enabling data-driven agriculture.
---

## 📌 Features

- 🌱 **Crop Recommendation** – Suggests the most suitable crop based on soil nutrients and weather conditions.
- 💊 **Fertilizer Prediction** – Recommends the best fertilizer using NPK values, soil type, and crop type.
- 🦠 **Plant Disease Detection** – Identifies crop diseases from leaf images using a pre-trained deep learning model.
- 👨‍🌾 **User Panel** – Register/login with JWT auth, update profile with photo.
- 🛠 **Admin Panel** – Upload and retrain datasets for crop/fertilizer modules.
- 🧠 **AI Models** – Integrated ML and DL models for prediction and classification.
- 📦 **MongoDB Integration** – Stores user data and profile information securely.
- 🔐 **JWT Authentication** – Token-based secure login system.

---

## 🧪 Technologies Used

- **Frontend**: React.js, Tailwind CSS
- **Backend**: Flask, Flask-JWT-Extended
- **Database**: MongoDB Atlas
- **ML/DL**: Scikit-learn, TensorFlow, OpenCV, NumPy
- **Others**: JWT Auth, Python dotenv, CORS, RESTful APIs

---

## 🗂 Dataset Sources

- **Crop Recommendation Dataset**  
  🔗 [Crop Recommendation - Kaggle](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)

- **Fertilizer Recommendation Dataset**  
  🔗 [Fertilizer Recommendation - Kaggle](https://www.kaggle.com/datasets/gdabhishek/fertilizer-prediction)

- **Plant Disease Detection Dataset**  
  🔗 [PlantVillage Dataset - Kaggle](https://www.kaggle.com/models/agripredict/disease-classification)

> 🧠 Plant Disease Detection is powered by a pre-trained deep learning model trained on the PlantVillage dataset and exported in `.pb` format.

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/croppulse.git
cd croppulse
