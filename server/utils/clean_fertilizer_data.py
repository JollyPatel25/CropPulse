import pandas as pd
import os

def clean_fertilizer_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(base_dir, ".."))
    raw_path = os.path.join(project_root, "data", "fertilizer", "Fertilizer Prediction.csv")

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Dataset not found at: {raw_path}")

    df = pd.read_csv(raw_path)

    # Drop duplicates and missing values
    df.drop_duplicates(inplace=True)
    df.dropna(inplace=True)

    # Standardize and clean column names
    df.columns = [col.strip().capitalize() for col in df.columns]
    df.rename(columns={
        "Temparature": "Temperature",
        "Fertilizer name": "Fertilizer Name",
        "Crop type": "Crop Type",
        "Soil type": "Soil Type"
    }, inplace=True)

    # Clip outliers in numeric fields
    for col in ['Temperature', 'Humidity', 'Moisture', 'Nitrogen', 'Potassium', 'Phosphorous']:
        if col in df.columns:
            df[col] = df[col].clip(lower=df[col].quantile(0.01), upper=df[col].quantile(0.99))

    # ✅ Replace fertilizer codes with readable names
    fertilizer_map = {
        "Urea": "Urea (46-0-0)",
        "DAP": "DAP (18-46-0)",
        "14-35-14": "NPK (14-35-14)",
        "28-28": "NPK (28-28-0)",
        "17-17-17": "NPK (17-17-17)",
        "20-20": "NPK (20-20-0)",
        "20-20": "NPK (20-20-0)",
        "20-20": "NPK (20-20-0)",
        "28-28": "NPK (28-28-0)",
        "10-26-26": "NPK (10-26-26)",
        "14-35-14": "NPK (14-35-14)",
        "17-17-17": "NPK (17-17-17)",
        "10-26-26": "NPK (10-26-26)"
    }

    df["Fertilizer Name"] = df["Fertilizer Name"].apply(lambda x: fertilizer_map.get(str(x), str(x)))

    # Save cleaned dataset
    df.to_csv(raw_path, index=False)
    print("Cleaned fertilizer data with readable fertilizer names saved.")

