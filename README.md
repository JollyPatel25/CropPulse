# 🌿 CropPulse - Smart Crop Advisory System

**CropPulse** is an AI-powered smart crop advisory system that assists farmers and agricultural experts in making informed, data-driven decisions. It offers intelligent crop recommendations, fertilizer suggestions, and plant disease detection—all through an intuitive interface designed for both farmers and admins.

---

## 📌 Key Features

- 🌱 **Crop Recommendation**  
  Suggests the most suitable crop based on soil nutrients (NPK), pH, temperature, humidity, and rainfall.

- 💊 **Fertilizer Prediction**  
  Recommends optimal fertilizers based on soil type, crop type, and nutrient values.

- 🦠 **Plant Disease Detection**  
  Detects diseases in crops from leaf images using a deep learning model trained on the PlantVillage dataset.

- 👨‍🌾 **User Panel**  
  - Secure registration and login (JWT-based)  
  - Update profile, including personal details and profile picture

- 🛠 **Admin Panel**  
  - Upload and manage crop and fertilizer datasets  
  - Trigger model retraining for better accuracy

- 🔐 **Authentication**  
  JWT-secured API endpoints with MongoDB-based user storage.

---
---

## 🧾 MongoDB Schema

### 📂 Collection: `users`

Each user is stored as a document in the `users` collection with the following schema:

```json
{
  "_id": ObjectId,
  "email": String,
  "password": String,         Hashed using scrypt
  "name": String,
  "birth_date": String,       Format: YYYY-MM-DD
  "address": {
    "street": String,
    "city": String,
    "state": String,
    "pincode": String
  },
  "role": String,             "user" or "admin"
  "profile_image": String     Filename of the uploaded image (stored in /uploads)
}
```

## 🧠 Tech Stack

- **Frontend**: React.js, Tailwind CSS  
- **Backend**: Flask, Flask-JWT-Extended  
- **Database**: MongoDB (local/Atlas)  
- **Machine Learning**: Scikit-learn, TensorFlow, OpenCV  
- **Others**: JWT, dotenv, CORS, REST API

---

## 🗂 Dataset Sources

- 🌾 [Crop Recommendation Dataset – Kaggle](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)  
- 💊 [Fertilizer Recommendation Dataset – Kaggle](https://www.kaggle.com/datasets/gdabhishek/fertilizer-prediction)  
- 🦠 [Plant Disease Detection (PlantVillage) – Kaggle](https://www.kaggle.com/models/agripredict/disease-classification)

> 🧠 Disease Detection is powered by a pre-trained `.pb` TensorFlow model trained on PlantVillage.

---
### NOTE:
### This project requires a working MongoDB connection. If you don’t provide a valid .env file with a working MongoDB URI, the backend will fail to connect and you'll receive errors. Use your own MongoDB Atlas or local connection string.
## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/CropPulse.git
cd CropPulse
