# utils/train_model.py

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import os

def train_crop_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # path to utils/
    project_root = os.path.abspath(os.path.join(base_dir, ".."))  # project root

    dataset_path = os.path.join(project_root, "data", "crop", "Crop_recommendation.csv")
    model_dir = os.path.join(project_root, "models")
    model_path = os.path.join(model_dir, "crop_model.pkl")

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at: {dataset_path}")

    df = pd.read_csv(dataset_path)
    X = df.drop('label', axis=1)
    y = df['label']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    os.makedirs(model_dir, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained and saved to {model_path}")
