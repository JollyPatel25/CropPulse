import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def train_fertilizer_model():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    dataset_path = os.path.join(project_root, "data", "fertilizer", "Fertilizer Prediction.csv")
    model_dir = os.path.join(project_root, "models")

    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, "fertilizer_model.pkl")
    fertilizer_enc_path = os.path.join(model_dir, "fertilizer_label_encoder.pkl")
    soil_enc_path = os.path.join(model_dir, "soil_label_encoder.pkl")
    crop_enc_path = os.path.join(model_dir, "crop_label_encoder.pkl")

    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset not found at: {dataset_path}")

    df = pd.read_csv(dataset_path)

    # Encode categorical columns
    fert_enc = LabelEncoder()
    soil_enc = LabelEncoder()
    crop_enc = LabelEncoder()

    df["Fertilizer Name"] = fert_enc.fit_transform(df["Fertilizer Name"])
    df["Soil Type"] = soil_enc.fit_transform(df["Soil Type"])
    df["Crop Type"] = crop_enc.fit_transform(df["Crop Type"])

    X = df.drop("Fertilizer Name", axis=1)
    y = df["Fertilizer Name"]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    # Save model and encoders
    joblib.dump(model, model_path)
    joblib.dump(fert_enc, fertilizer_enc_path)
    joblib.dump(soil_enc, soil_enc_path)
    joblib.dump(crop_enc, crop_enc_path)

    print("Fertilizer model and encoders saved successfully.")

if __name__ == "__main__":
    train_fertilizer_model()
