import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
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

    # ✅ Split the dataset into train and test
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # ✅ Train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # ✅ Predict on test set
    y_pred = model.predict(X_test)

    # ✅ Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy on Test Set: {accuracy:.4f}",flush=True)  # e.g., 0.9825

    # ✅ Save the model
    os.makedirs(model_dir, exist_ok=True)
    with open(model_path, "wb") as f:
        pickle.dump(model, f)

    print(f"Model trained and saved to {model_path}")
