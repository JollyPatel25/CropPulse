# utils/clean_crop_data.py

import pandas as pd
import os

def clean_crop_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))

    raw_path = os.path.join(project_root, "data", "crop", "Crop_recommendation.csv")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Dataset not found at: {raw_path}")

    df = pd.read_csv(raw_path)

    # 🔍 Sample cleaning operations:
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Optionally: remove outliers, fix values, normalize, etc.
    # Example: cap outliers
    for col in ['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']:
        df[col] = df[col].clip(lower=df[col].quantile(0.01), upper=df[col].quantile(0.99))

    # Save cleaned file (overwrite or new)
    df.to_csv(raw_path, index=False)
    print(" Cleaned data saved.")
