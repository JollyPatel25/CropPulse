import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
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

    # ✅ Split into training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # ✅ Predict on test set
    y_pred = model.predict(X_test)

    # ✅ Calculate and print accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}",flush=True)

    # ✅ Optional: Classification report
    print("\nClassification Report:", flush=True )
    print(classification_report(y_test, y_pred, target_names=fert_enc.classes_, zero_division=0), flush=True)


    joblib.dump(model, model_path)
    joblib.dump(fert_enc, fertilizer_enc_path)
    joblib.dump(soil_enc, soil_enc_path)
    joblib.dump(crop_enc, crop_enc_path)

    print("Fertilizer model and encoders saved successfully.", flush=True)

if __name__ == "__main__":
    train_fertilizer_model()




# import pandas as pd
# from sklearn.ensemble import RandomForestClassifier
# from sklearn.preprocessing import LabelEncoder
# import joblib
# import os

# def train_fertilizer_model():
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     project_root = os.path.abspath(os.path.join(base_dir, ".."))

#     dataset_path = os.path.join(project_root, "data", "fertilizer", "Fertilizer Prediction.csv")
#     model_dir = os.path.join(project_root, "models")

#     os.makedirs(model_dir, exist_ok=True)

#     model_path = os.path.join(model_dir, "fertilizer_model.pkl")
#     fertilizer_enc_path = os.path.join(model_dir, "fertilizer_label_encoder.pkl")
#     soil_enc_path = os.path.join(model_dir, "soil_label_encoder.pkl")
#     crop_enc_path = os.path.join(model_dir, "crop_label_encoder.pkl")

#     if not os.path.exists(dataset_path):
#         raise FileNotFoundError(f"Dataset not found at: {dataset_path}")

#     df = pd.read_csv(dataset_path)

#     # Encode categorical columns
#     fert_enc = LabelEncoder()
#     soil_enc = LabelEncoder()
#     crop_enc = LabelEncoder()

#     df["Fertilizer Name"] = fert_enc.fit_transform(df["Fertilizer Name"])
#     df["Soil Type"] = soil_enc.fit_transform(df["Soil Type"])
#     df["Crop Type"] = crop_enc.fit_transform(df["Crop Type"])

#     X = df.drop("Fertilizer Name", axis=1)
#     y = df["Fertilizer Name"]

#     model = RandomForestClassifier(n_estimators=100, random_state=42)
#     model.fit(X, y)

#     # Save model and encoders
#     joblib.dump(model, model_path)
#     joblib.dump(fert_enc, fertilizer_enc_path)
#     joblib.dump(soil_enc, soil_enc_path)
#     joblib.dump(crop_enc, crop_enc_path)

#     print("Fertilizer model and encoders saved successfully.")

# if __name__ == "__main__":
#     train_fertilizer_model()
